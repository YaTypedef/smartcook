CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

SET(THRIFT_DIR ${CMAKE_CURRENT_LIST_DIR})
SET(THRIFT_FILE ${THRIFT_DIR}/search.thrift)

FIND_PROGRAM(THRIFT_BIN thrift /bin /usr/bin /usr/local/bin)

IF(THRIFT_BIN)
    IF(EXISTS ${THRIFT_FILE})
        MESSAGE("Compiling ${THRIFT_FILE}")
        EXECUTE_PROCESS(
            COMMAND ${THRIFT_BIN} "-r" "--gen" "cpp" "-o" "${CMAKE_CURRENT_LIST_DIR}" "${THRIFT_FILE}"
            WORKING_DIRECTORY .
            RESULT_VARIABLE RESULT)
        MESSAGE("Result ${RESULT}")
    ELSE(EXISTS ${THRIFT_FILE})
        MESSAGE(SEND_ERROR "Could not find file to compile.")
    ENDIF(EXISTS ${THRIFT_FILE})
ELSE(THRIFT_BIN)
    MESSAGE(SEND_ERROR "Could not find thrift binary.")
ENDIF(THRIFT_BIN)
