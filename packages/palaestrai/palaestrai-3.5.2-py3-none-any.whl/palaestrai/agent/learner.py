"""This module contains the abstract class :class:`Brain` that is used
to implement the thinking part of agents.

"""

from __future__ import annotations

from asyncio import Future

import asyncio
import logging
import numpy as np
import uuid
from abc import ABC
from typing import TYPE_CHECKING, List, Optional

from palaestrai.core import EventStateMachine as ESM
from palaestrai.core.protocol import (
    MuscleUpdateRequest,
    MuscleUpdateResponse,
    MuscleShutdownRequest,
    MuscleShutdownResponse,
)
from .memory import Memory

LOG = logging.getLogger(__name__)

if TYPE_CHECKING:
    from . import SensorInformation, ActuatorInformation, Objective, Brain


@ESM.monitor(is_mdp_worker=True)
class Learner:
    """Runtime wrapper for :class:`Brain`s.

    A :class:`Brain` is the learning implementation of an algorithm, be it
    deep reinforcement learning or any other kind of algorithm.
    However, a algorithm developers that implements a :class:`Brain` does not
    need to concern themselves with the inner workings of palaestrAI, e.g.,
    the major domo broker and the messaging protocol.
    Therefore, :class:`Brain` instances are wrapped in Learner objects that
    take care of the communication and all the many things that can possibly
    go wrong.

    Parameters
    ----------
    brain : Brain
        The actual :class:`Brain` instance this Learner wraps
    uid : str
        The unique ID of the :class:`Brain` (for communications mostly)
    """

    def __init__(self, brain: Brain, uid: str):
        self._uid: str = uid
        self._brain: Brain = brain

    @property
    def uid(self):
        """Unique ID of this Brain"""
        return self._uid

    @property
    def brain(self) -> Brain:
        """The :clasS:`Brain` this Learner caters for"""
        return self._brain

    def setup(self):
        """Internal setup method of the Brain

        This method initializes the brain before the main loop (run) is called.
        It sets up the signal handlers, tries to load the brain dump, and
        sets the state to ::`State.RUNNING`.

        The internal setup method does not provide a hook for setup of
        derived brain classes. If you want to implement such a hook, implement
        the public :meth:`~Brain.setup` method.
        """
        assert self._brain is not None

        self._brain.try_load_brain_dump()
        self._brain.setup()

        # noinspection PyAttributeOutsideInit
        self.mdp_service = self.uid

    @ESM.on(MuscleUpdateRequest)
    async def _handle_muscle_update_request(
        self, request: MuscleUpdateRequest
    ) -> MuscleUpdateResponse:
        assert self._brain is not None

        LOG.debug(
            "%s will think about that " "breaking new %s that just arrived.",
            self,
            request,
        )
        self._brain.memory.append(
            muscle_uid=request.sender_rollout_worker_id,
            sensor_readings=request.sensor_readings,
            actuator_setpoints=request.actuator_setpoints,
            rewards=request.rewards,
            objective=np.array([request.objective]),
            done=request.done,
        )
        potential_update = self._brain.thinking(
            muscle_id=request.sender_rollout_worker_id,
            data_from_muscle=request.data,
        )

        response = MuscleUpdateResponse(
            sender_brain_id=request.receiver_brain_id,
            receiver_muscle_id=request.sender_rollout_worker_id,
            experiment_run_id=request.experiment_run_id,
            experiment_run_phase=request.experiment_run_phase,
            experiment_run_instance_id=request.experiment_run_instance_id,
            update=potential_update,
        )
        return response

    @ESM.on(MuscleShutdownRequest)
    async def _handle_muscle_shutdown_request(
        self, request: MuscleShutdownRequest
    ):
        assert self._brain is not None

        LOG.info(
            "%s saw its only muscle requesting a break.",
            self,
        )
        self._brain.store()

        # TODO: Handle multiple Muscles for a Brain
        # noinspection PyUnresolvedReferences
        self.stop()  # type: ignore[attr-defined]

        LOG.info("%s completed shutdown.", self)

        return MuscleShutdownResponse(
            sender_brain_id=request.receiver_brain_id,
            receiver_muscle_id=request.sender_muscle_id,
            experiment_run_id=request.experiment_run_id,
            experiment_run_instance_id=request.experiment_run_instance_id,
            experiment_run_phase=request.experiment_run_phase,
        )

    def __str__(self):
        return "%s(id=0x%x, uid=%s)" % (self.__class__, id(self), self._uid)
