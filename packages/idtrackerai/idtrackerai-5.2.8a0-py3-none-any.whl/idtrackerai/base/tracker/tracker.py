import logging

import numpy as np

from idtrackerai import ListOfFragments, ListOfGlobalFragments, Session
from idtrackerai.utils import IdtrackeraiError, conf, create_dir

from ..network import CNN, DEVICE, LearnerClassification, NetworkParams
from .accumulation_manager import AccumulationManager
from .accumulator import perform_one_accumulation_step
from .assigner import assign_remaining_fragments
from .identity_transfer import identify_first_global_fragment_for_accumulation
from .pre_trainer import pretrain_global_fragment


class TrackerAPI:
    "API for tracking with identities more than one animal with more than one Global Fragment"

    identification_model: CNN
    accumulation_network_params: NetworkParams

    def __init__(
        self,
        session: Session,
        list_of_fragments: ListOfFragments,
        list_of_global_fragments: ListOfGlobalFragments,
    ):
        self.session = session
        self.list_of_fragments = list_of_fragments
        self.list_of_global_fragments = list_of_global_fragments

    def track(self) -> ListOfFragments:
        """In protocol 3, list_of_fragments is loaded from accumulation
        folders so the reference from outside tracker_API is lost.
        That's why list_of_fragments has to be returned"""
        logging.info("Tracking with identities")
        self.session.create_accumulation_folder(iteration_number=0, delete=True)
        self.accumulation_network_params = NetworkParams(
            n_classes=self.session.n_animals,
            save_folder=self.session.accumulation_folder,
            knowledge_transfer_folder=self.session.knowledge_transfer_folder,
            model_name="identification_network",
            image_size=self.session.id_image_size,
            optimizer="SGD",
            schedule=[30, 60],
            optim_args={"lr": conf.LEARNING_RATE_IDCNN_ACCUMULATION, "momentum": 0.9},
            epochs=conf.MAXIMUM_NUMBER_OF_EPOCHS_IDCNN,
        )
        self.accumulation_network_params.save()
        self.protocol1()
        return self.list_of_fragments

    def protocol1(self):
        self.session.protocol1_timer.start()

        self.list_of_fragments.reset(roll_back_to="fragmentation")

        if self.session.knowledge_transfer_folder:
            try:
                self.identification_model = LearnerClassification.load_model(
                    self.accumulation_network_params, knowledge_transfer=True
                )
                logging.info("Tracking with knowledge transfer")
                if not self.session.identity_transfer:
                    self.identification_model.fully_connected_reinitialization()
                else:
                    logging.info(
                        "Identity transfer. Not reinitializing the fully connected"
                        " layers."
                    )
            except RuntimeError as exc:
                logging.error(
                    f"Could not load model {self.accumulation_network_params} to"
                    " transfer knowledge from, following without knowledge nor identity"
                    " transfer.\n"
                    f"Raised error: {exc}"
                )
                self.identification_model = CNN.from_network_params(
                    self.accumulation_network_params
                ).to(DEVICE)
        else:
            self.identification_model = CNN.from_network_params(
                self.accumulation_network_params
            ).to(DEVICE)

        first_global_fragment = max(
            self.list_of_global_fragments, key=lambda gf: gf.minimum_distance_travelled
        )

        self.session.first_frame_first_global_fragment.append(
            first_global_fragment.first_frame_of_the_core
        )

        identify_first_global_fragment_for_accumulation(
            first_global_fragment,
            self.session,
            identification_model=self.identification_model,
        )

        self.session.identities_groups = self.list_of_fragments.build_exclusive_rois()

        # Order global fragments by distance to the first global fragment for the accumulation
        self.list_of_global_fragments.sort_by_distance_to_the_frame(
            first_global_fragment.first_frame_of_the_core
        )

        # Instantiate accumulation manager
        self.accumulation_manager = AccumulationManager(
            self.session.n_animals,
            self.list_of_fragments,
            self.list_of_global_fragments,
        )

        # Selecting the first global fragment is considered as
        # the 0 accumulation step
        self.accumulate()

    def accumulate(self):
        logging.info("Entering accumulation loop")
        if self.accumulation_manager.new_global_fragments_for_training:
            # Training and identification continues
            if (
                self.accumulation_manager.current_step == 1
                and self.session.accumulation_trial == 0
            ):
                # first training finished
                self.session.protocol1_timer.finish()
                self.session.protocol2_timer.start()

            # Training and identification step
            perform_one_accumulation_step(
                self.accumulation_manager,
                self.session,
                self.identification_model,
                self.accumulation_network_params,
            )
            # Re-enter the function for the next step of the accumulation
            self.accumulate()
            return

        if (
            not self.session.protocol2_timer.finished
            and self.accumulation_manager.ratio_accumulated_images
            > conf.THRESHOLD_EARLY_STOP_ACCUMULATION
        ):
            # Accumulation stop because protocol 1 is successful
            self.save_after_first_accumulation()
            self.session.protocol1_timer.finish()
            logging.info("Protocol 1 successful")
            assign_remaining_fragments(
                self.list_of_fragments,
                self.identification_model,
                self.accumulation_network_params,
                self.session.identify_timer,
            )
            return

        if not self.session.protocol3_pretraining_timer.finished:
            logging.info("No more new global fragments")
            self.save_after_first_accumulation()

            if (
                self.accumulation_manager.ratio_accumulated_images
                >= conf.THRESHOLD_ACCEPTABLE_ACCUMULATION
            ):
                self.session.protocol2_timer.finish()
                logging.info("Protocol 2 successful")
                assign_remaining_fragments(
                    self.list_of_fragments,
                    self.identification_model,
                    self.accumulation_network_params,
                    self.session.identify_timer,
                )
                return

            self.session.protocol1_timer.finish()
            self.session.protocol2_timer.finish(raise_if_not_started=False)
            logging.warning(
                "[red]Protocol 2 failed, protocol 3 is going to start",
                extra={"markup": True},
            )
            ask_about_protocol3(
                self.session.protocol3_action, self.session.number_of_error_frames
            )
            self.pretrain()
            self.accumulate()
            return

        if (
            self.session.accumulation_trial
            < conf.MAXIMUM_NUMBER_OF_PARACHUTE_ACCUMULATIONS
            and self.accumulation_manager.ratio_accumulated_images
            < conf.THRESHOLD_ACCEPTABLE_ACCUMULATION
        ):
            logging.warning("Accumulation Protocol 3 failed. Opening parachute ...")
            if self.session.accumulation_trial == 0:
                self.session.protocol3_accumulation_timer.start()
            else:
                self.save_and_update_accumulation_parameters_in_parachute()
            self.session.accumulation_trial += 1
            self.accumulation_parachute_init(self.session.accumulation_trial)
            self.accumulate()
            return

        logging.info("Accumulation after protocol 3 has been successful")
        self.session.protocol3_accumulation_timer.finish()

        self.save_after_second_accumulation()
        assign_remaining_fragments(
            self.list_of_fragments,
            self.identification_model,
            self.accumulation_network_params,
            self.session.identify_timer,
        )

    def save_after_first_accumulation(self):
        """Set flags and save data"""
        logging.info("Saving first accumulation parameters")

        # if not self.restoring_first_accumulation:
        self.session.ratio_accumulated_images = (
            self.accumulation_manager.ratio_accumulated_images
        )
        self.session.percentage_of_accumulated_images = [
            self.session.ratio_accumulated_images
        ]
        self.session.save()
        self.list_of_fragments.save(self.session.fragments_path)
        self.list_of_fragments.save(self.session.accumulation_folder)
        self.list_of_global_fragments.save(self.session.global_fragments_path)

    def pretrain(self):
        self.session.protocol3_pretraining_timer.start()
        create_dir(self.session.pretraining_folder, remove_existing=True)

        pretrain_network_params = NetworkParams(
            n_classes=self.session.n_animals,
            save_folder=self.session.pretraining_folder,
            model_name="identification_network",
            image_size=self.session.id_image_size,
            optimizer="SGD",
            schedule=[30, 60],
            optim_args={"lr": conf.LEARNING_RATE_IDCNN_ACCUMULATION, "momentum": 0.9},
            epochs=conf.MAXIMUM_NUMBER_OF_EPOCHS_IDCNN,
            knowledge_transfer_folder=self.session.knowledge_transfer_folder,
        )
        pretrain_network_params.save()

        # Initialize network
        if pretrain_network_params.knowledge_transfer_folder:
            self.identification_model = LearnerClassification.load_model(
                pretrain_network_params, knowledge_transfer=True
            )
            self.identification_model.fully_connected_reinitialization()
        else:
            self.identification_model = CNN.from_network_params(
                pretrain_network_params
            ).to(DEVICE)

        self.list_of_fragments.reset(roll_back_to="fragmentation")
        self.list_of_global_fragments.sort_by_distance_travelled()

        pretraining_counter = -1
        ratio_of_pretrained_images = 0.0
        while ratio_of_pretrained_images < conf.MAX_RATIO_OF_PRETRAINED_IMAGES:
            pretraining_counter += 1
            logging.info(
                "[bold]New pretraining iteration[/], using the #%s global fragment",
                pretraining_counter,
                extra={"markup": True},
            )
            pretrain_global_fragment(
                self.identification_model,
                pretrain_network_params,
                self.list_of_global_fragments.global_fragments[pretraining_counter],
                self.session.id_images_file_paths,
            )
            ratio_of_pretrained_images = (
                self.list_of_fragments.ratio_of_images_used_for_pretraining
            )

            logging.debug(
                f"{ratio_of_pretrained_images:.2%} of the images have been used during"
                " pretraining (if higher than"
                f" {conf.MAX_RATIO_OF_PRETRAINED_IMAGES:.2%} we stop pretraining)"
            )

        self.session.protocol3_pretraining_timer.finish()

    """ parachute """

    def accumulation_parachute_init(self, iteration_number: int):
        logging.debug("Accumulation_parachute_init")
        logging.info("Starting accumulation %i", iteration_number)

        # delete = not self.processes_to_restore.get("protocol3_accumulation")

        self.session.create_accumulation_folder(
            iteration_number=iteration_number, delete=True
        )
        self.session.accumulation_trial = iteration_number
        self.list_of_fragments.reset(roll_back_to="fragmentation")

        logging.info(
            "Setting #%d global fragment for accumulation", iteration_number - 1
        )

        self.list_of_global_fragments.sort_by_distance_travelled()
        try:
            first_global_fragment = self.list_of_global_fragments.global_fragments[
                iteration_number - 1
            ]
        except IndexError:
            first_global_fragment = None  # TODO what if this happens

        self.session.first_frame_first_global_fragment.append(
            first_global_fragment.first_frame_of_the_core
            if first_global_fragment is not None
            else None
        )

        if first_global_fragment is not None:
            identify_first_global_fragment_for_accumulation(
                first_global_fragment,
                self.session,
                (
                    LearnerClassification.load_model(self.accumulation_network_params)
                    if self.session.identity_transfer
                    else None
                ),
            )
        self.session.identities_groups = self.list_of_fragments.build_exclusive_rois()

        # Sort global fragments by distance
        self.list_of_global_fragments.sort_by_distance_to_the_frame(
            self.session.first_frame_first_global_fragment[iteration_number - 1]
        )
        logging.warning(
            "first_frame_first_global_fragment %s",
            self.session.first_frame_first_global_fragment,
        )
        logging.info(
            "We will restore the network from a previous pretraining: %s",
            self.session.pretraining_folder,
        )

        # Set saving folders
        self.accumulation_network_params.save_folder = self.session.accumulation_folder

        # Set restoring model_file
        self.accumulation_network_params.restore_folder = (
            self.session.pretraining_folder
        )

        # TODO: allow to train only the fully connected layers

        self.identification_model = LearnerClassification.load_model(
            self.accumulation_network_params
        )

        self.identification_model.fully_connected_reinitialization()

        # Instantiate accumualtion manager
        self.accumulation_manager = AccumulationManager(
            self.session.n_animals,
            self.list_of_fragments,
            self.list_of_global_fragments,
        )

        logging.info("Start accumulation")

    def save_and_update_accumulation_parameters_in_parachute(self):
        logging.info(
            "Accumulated images"
            f" {self.accumulation_manager.ratio_accumulated_images:.2%}"
        )
        self.session.ratio_accumulated_images = (
            self.accumulation_manager.ratio_accumulated_images
        )
        self.session.percentage_of_accumulated_images.append(
            self.session.ratio_accumulated_images
        )
        self.list_of_fragments.save(
            self.session.accumulation_folder / "list_of_fragments.json"
        )

    def save_after_second_accumulation(self):
        logging.info("Saving second accumulation parameters")
        # Save accumulation parameters
        self.save_and_update_accumulation_parameters_in_parachute()

        # Choose best accumulation
        self.session.accumulation_trial = int(
            np.argmax(self.session.percentage_of_accumulated_images)
        )

        # Update ratio of accumulated images and  accumulation folder
        self.session.ratio_accumulated_images = (
            self.session.percentage_of_accumulated_images[
                self.session.accumulation_trial
            ]
        )
        self.session.create_accumulation_folder(
            iteration_number=self.session.accumulation_trial
        )

        # Load light list of fragments with identities of the best accumulation
        self.list_of_fragments = ListOfFragments.load(
            self.session.auto_accumulation_folder / "list_of_fragments.json"
        )

        # Save objects
        self.list_of_fragments.save(self.session.fragments_path)
        self.list_of_global_fragments.save(self.session.global_fragments_path)

        # set restoring folder
        logging.info("Restoring networks to best second accumulation")
        self.accumulation_network_params.restore_folder = (
            self.session.accumulation_folder
        )

        # TODO: allow to train only the fully connected layers

        # Load pretrained network
        self.identification_model = LearnerClassification.load_model(
            self.accumulation_network_params
        )

        # # Re-initialize fully-connected layers
        # self.identification_model.apply(fc_weights_reinit)

        self.session.save()


def ask_about_protocol3(protocol3_action: str, n_error_frames: int) -> None:
    """Raises a IdtrackeraiError if protocol3_action is abort or aks and user answers abortion"""
    logging.info("Protocol 3 action: %s", protocol3_action)

    if protocol3_action == "abort":
        raise IdtrackeraiError(
            "Protocol 3 was going to start but PROTOCOL3_ACTION is set to 'abort'"
        )
    if protocol3_action == "continue":
        return

    if protocol3_action != "ask":
        raise ValueError(
            f'PROTOCOL3_ACTION "{protocol3_action}" not in ("ask", "abort", "continue")'
        )

    if n_error_frames > 0:
        logging.info(
            "Protocol 3 is a very time consuming algorithm and, in most cases, it"
            " can be avoided by redefining the segmentation parameters. As"
            " [red]there are %d frames with more blobs than animals[/red], we"
            " recommend you to abort the tracking session now and go back to the"
            " Segmentation app focusing on not having reflections, shades, etc."
            " detected as blobs. Check the following general recommendations:\n   "
            " - Define a region of interest to exclude undesired noise blobs\n    -"
            " Shrink the intensity (or background difference) thresholds\n    -"
            " Toggle the use of the background subtraction\n    - Shrink the blob's"
            " area thresholds",
            n_error_frames,
            extra={"markup": True},
        )
    else:
        logging.info(
            "Protocol 3 is a very time consuming algorithm and, in most cases, it"
            " can be avoided by redefining the segmentation parameters. As"
            " [bold]there are NOT frames with more blobs than animals[/bold], the"
            " video is unlikely to have non-animal blobs. Even so, you can choose"
            " to abort the tracking session and redefine the segmentation"
            " parameters (specially shrinking the intensity (or background"
            " difference) thresholds) or to continue with Protocol 3.",
            extra={"markup": True},
        )

    abort = None
    valid_answers = {"abort": True, "a": True, "continue": False, "c": False}
    while abort is None:
        answer_str = input(
            "What do you want to do now? Abort [A] or Continue [C]? "
        ).lower()
        if answer_str not in valid_answers:
            logging.warning("Invalid answer")
            continue
        abort = valid_answers[answer_str]
        logging.info("Answer --> Abort? %s", abort)
    if abort:
        raise IdtrackeraiError(
            "This is not an actual error: protocol 3 was going to start"
            " but PROTOCOL3_ACTION is set to 'ask' and used aborted."
        )
    return
