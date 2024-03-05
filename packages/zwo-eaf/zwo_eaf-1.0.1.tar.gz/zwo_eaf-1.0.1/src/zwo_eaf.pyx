# zwo_eaf.pyx

cimport zwo_eaf

def _error_code_to_string(int error_code):
    codes = {
        0: "SUCCESS",
        1: "INVALID_INDEX",
        2: "INVALID_ID",
        3: "INVALID_VALUE",
        4: "REMOVED",
        5: "MOVING",
        6: "ERROR_STATE",
        7: "GENERAL_ERROR",
        8: "NOT_SUPPORTED",
        9: "CLOSED",
        -1: "END"
    }
    if error_code in codes:
        return codes[error_code]
    else:
        return f"UNKNOWN ({error_code})"

def getNumEAFs():
    return zwo_eaf.EAFGetNum()

def getEAFID(int index):
    cdef int ID
    error_code = zwo_eaf.EAFGetID(index, &ID)
    if error_code != zwo_eaf.EAF_ERROR_CODE.EAF_SUCCESS:
        raise ValueError(f"Error getting EAF ID. Code: {_error_code_to_string(error_code)}")
    return ID


cdef enum EAF_MOVING_STATUS:
    NOT_MOVING
    MOVING
    MOVING_WITH_HANDLE


cdef class EAF:
    cdef int ID
    cdef int _max_step

    def __cinit__(self, int ID):
        self.ID = ID
        zwo_eaf.EAFOpen(self.ID)
        cdef int max_step
        zwo_eaf.EAFGetMaxStep(self.ID, &max_step)
        self._max_step = max_step

    def __dealloc__(self):
        zwo_eaf.EAFClose(self.ID)

    def get_max_step(self):
        return self._max_step

    def move_to(self, int step):
        assert 0 <= step <= self._max_step, f"Position {step} is out of range [0, {self._max_step}]"
        error_code = zwo_eaf.EAFMove(self.ID, step)
        if error_code != zwo_eaf.EAF_ERROR_CODE.EAF_SUCCESS:
            raise ValueError(f"Error with EAF move. Code: {_error_code_to_string(error_code)}")

    def stop(self):
        error_code = zwo_eaf.EAFStop(self.ID)
        if error_code != zwo_eaf.EAF_ERROR_CODE.EAF_SUCCESS:
            raise ValueError(f"Error stopping EAF. Code: {_error_code_to_string(error_code)}")

    def get_moving_status(self):
        '''
        Returns the moving status of the focuser.
        The 3 states are NOT_MOVING, MOVING, and MOVING_WITH_HANDLE.
        NOT_MOVING: The focuser is not moving.
        MOVING: The focuser is moving, but it can be stopped by the `stop()` method.
        MOVING_WITH_HANDLE: The focuser is moving, and it cannot be stopped by the `stop()` method.
        '''
        cdef int moving, handle_controlled # these are bools but I can't figure out how to get it to compile with bool or bint. 
        error_code = zwo_eaf.EAFIsMoving(self.ID, &moving, &handle_controlled)
        if error_code != zwo_eaf.EAF_ERROR_CODE.EAF_SUCCESS:
            raise ValueError(f"Error checking if EAF is moving. Code: {_error_code_to_string(error_code)}")
        if moving and handle_controlled:
            return EAF_MOVING_STATUS.MOVING_WITH_HANDLE
        elif moving:
            return EAF_MOVING_STATUS.MOVING
        else:
            return EAF_MOVING_STATUS.NOT_MOVING
    
    def is_moving(self):
        '''
        Returns True if the focuser is moving, False otherwise.

        This thing is inconsistent as hell. It's better to just check if
        the position is changing, or if it's reached the target position and then
        call `stop()`.
        '''
        return self.get_moving_status() != EAF_MOVING_STATUS.NOT_MOVING

    def get_position(self):
        cdef int position
        error_code = zwo_eaf.EAFGetPosition(self.ID, &position)
        if error_code != zwo_eaf.EAF_ERROR_CODE.EAF_SUCCESS:
            raise ValueError(f"Error getting EAF position. Code: {_error_code_to_string(error_code)}")
        return position

