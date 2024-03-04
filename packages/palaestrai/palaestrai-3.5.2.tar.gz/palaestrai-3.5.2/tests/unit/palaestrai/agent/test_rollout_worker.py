from unittest.async_case import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock

from palaestrai.agent import (
    SensorInformation,
    ActuatorInformation,
    DummyMuscle,
    DummyObjective,
    RewardInformation,
)
from palaestrai.agent import RolloutWorker
from palaestrai.core import MajorDomoWorker, MajorDomoClient
from palaestrai.core.protocol import (
    AgentUpdateRequest,
    AgentShutdownRequest,
    MuscleUpdateResponse,
    MuscleShutdownResponse,
    MuscleUpdateRequest,
    MuscleShutdownRequest,
    AgentShutdownResponse,
    AgentUpdateResponse,
    EnvironmentResetNotificationRequest,
    EnvironmentResetNotificationResponse,
)
from palaestrai.types import Mode, Discrete


class TestRolloutWorker(IsolatedAsyncioTestCase):
    def setUp(self):
        self.muscle = DummyMuscle()
        self.muscle._uid = "muscle-id"

        self.rollout_worker = RolloutWorker(
            brain_uid="brain-id",
            muscle=self.muscle,
            objective=DummyObjective({}),
            uid="worker-id",
        )
        self.rollout_worker._experiment_run_id = "run-id"
        self.rollout_worker._experiment_run_instance_id = "run-instance-id"
        self.rollout_worker._experiment_run_phase = 42

    @patch(
        "palaestrai.agent.dummy_muscle.DummyMuscle.propose_actions",
        return_value=(
            ActuatorInformation(2, Discrete(4), "0"),
            ActuatorInformation(2, Discrete(4), "0"),
            [0, 1, 2],
            {},
        ),
    )
    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=AsyncMock(
            transceive=AsyncMock(
                side_effect=[
                    AgentUpdateRequest(
                        sender_simulation_controller_id="0815",
                        receiver_rollout_worker_id="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_instance_id="exp_42_instance",
                        experiment_run_phase=42,
                        actuators=[ActuatorInformation(0, Discrete(2), "0")],
                        sensors=[SensorInformation(1, Discrete(2), "0")],
                        rewards=[RewardInformation(7, Discrete(10), "Test")],
                        is_terminal=False,
                        mode=Mode.TRAIN,
                    ),
                    AgentShutdownRequest(
                        sender="0185",
                        receiver="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_phase=42,
                        experiment_run_instance_id="exp_42_instance",
                    ),
                    None,
                ]
            )
        ),
    )
    @patch(
        "palaestrai.core.event_state_machine.MajorDomoClient",
        return_value=AsyncMock(
            send=AsyncMock(
                side_effect=[
                    MuscleUpdateResponse(
                        update=[0, 0, 0],
                        sender_brain_id="brain-id",
                        receiver_muscle_id="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_instance_id="exp_42_instance",
                        experiment_run_phase=42,
                    ),
                    MuscleShutdownResponse(
                        sender_brain_id="brain-id",
                        receiver_muscle_id="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_instance_id="exp_42_instance",
                        experiment_run_phase=42,
                    ),
                ]
            )
        ),
    )
    async def test_handle_agent_update(
        self,
        major_domo_client: MajorDomoClient,
        major_domo_worker: MajorDomoWorker,
        dummy_muscle_propose_actions,
    ):
        # noinspection PyUnresolvedReferences
        await self.rollout_worker.run()  # type: ignore[attr-defined]

        # noinspection PyUnresolvedReferences
        agent_update_client_calls = self.rollout_worker.__esm__._mdp_client.mock_calls  # type: ignore[attr-defined]
        self.assertEqual(
            2,
            len(agent_update_client_calls),
        )
        self.assertEqual(
            [MuscleUpdateRequest, MuscleShutdownRequest],
            [x.args[1].__class__ for x in agent_update_client_calls],
        )
        self.assertIsInstance(
            # noinspection PyUnresolvedReferences
            self.rollout_worker.__esm__._mdp_worker.transceive.mock_calls[1].args[0],  # type: ignore[attr-defined]
            AgentUpdateResponse,
            AgentShutdownResponse,
        )

    @patch(
        "palaestrai.agent.dummy_muscle.DummyMuscle.propose_actions",
        side_effect=RuntimeError("Booh!"),
    )
    async def test_handles_errors_in_propose_actions(
        self, dummy_muscle_propose_actions
    ):
        self.rollout_worker._done = False
        env_actions = RolloutWorker.try_propose_actions(
            self.rollout_worker._muscle, [], []
        )
        self.assertEqual(env_actions, ([], None))

    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=AsyncMock(
            transceive=AsyncMock(
                side_effect=[
                    EnvironmentResetNotificationRequest(
                        sender_simulation_controller_id="0815",
                        receiver_agent_id="muscle-id",
                    ),
                    AgentShutdownRequest(
                        sender="0815",
                        receiver="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_instance_id="exp_42_instance",
                        experiment_run_phase=47,
                    ),
                ]
            )
        ),
    )
    @patch(
        "palaestrai.core.event_state_machine.MajorDomoClient",
        return_value=AsyncMock(
            send=AsyncMock(
                side_effect=[
                    MuscleShutdownResponse(
                        sender_brain_id="brain-id",
                        receiver_muscle_id="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_instance_id="exp_42_instance",
                        experiment_run_phase=47,
                    )
                ]
            )
        ),
    )
    async def test_env_reset(
        self,
        major_domo_client: MajorDomoClient,
        major_domo_worker: MajorDomoWorker,
    ):
        # noinspection PyUnresolvedReferences
        await self.rollout_worker.run()  # type: ignore[attr-defined]

        # noinspection PyUnresolvedReferences
        agent_update_client_calls = self.rollout_worker.__esm__._mdp_client.mock_calls  # type: ignore[attr-defined]
        self.assertEqual(
            1,
            len(agent_update_client_calls),
        )
        self.assertEqual(
            [MuscleShutdownRequest],
            [x.args[1].__class__ for x in agent_update_client_calls],
        )

        self.assertIsInstance(
            # noinspection PyUnresolvedReferences
            self.rollout_worker.__esm__._mdp_worker.transceive.mock_calls[1].args[0],  # type: ignore[attr-defined]
            EnvironmentResetNotificationResponse,
        )

    @patch("palaestrai.agent.dummy_muscle.DummyMuscle.prepare_model")
    @patch(
        "palaestrai.core.event_state_machine.MajorDomoWorker",
        return_value=AsyncMock(
            transceive=AsyncMock(
                side_effect=[
                    AgentShutdownRequest(
                        sender="0815",
                        receiver="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_instance_id="exp_42_instance",
                        experiment_run_phase=47,
                    ),
                ]
            )
        ),
    )
    @patch(
        "palaestrai.core.event_state_machine.MajorDomoClient",
        return_value=AsyncMock(
            send=AsyncMock(
                side_effect=[
                    MuscleShutdownResponse(
                        sender_brain_id="brain-id",
                        receiver_muscle_id="muscle-id",
                        experiment_run_id="exp_42",
                        experiment_run_instance_id="exp_42_instance",
                        experiment_run_phase=47,
                    ),
                ]
            )
        ),
    )
    async def test_preparing_model(
        self,
        major_domo_client: MajorDomoClient,
        major_domo_worker: MajorDomoWorker,
        prepare_model,
    ):
        self.rollout_worker
        self.rollout_worker._muscle._mode = Mode.TEST

        # noinspection PyUnresolvedReferences
        await self.rollout_worker.run()  # type: ignore[attr-defined]

        self.assertTrue(prepare_model.called)
        self.assertTrue(self.rollout_worker._model_loaded)
