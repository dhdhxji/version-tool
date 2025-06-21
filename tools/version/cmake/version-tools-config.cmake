set(VERSION_TOOL_DIR "${CMAKE_CURRENT_LIST_DIR}/..")

function(template_version VERSION_FILE TEMPLATE OUTPUT)

    add_custom_command(
        OUTPUT ${OUTPUT}
        COMMAND python3 ${VERSION_TOOL_DIR}/version_tools.py 
                        ${VERSION_FILE}
                        ${TEMPLATE}
                        ${OUTPUT}
        MAIN_DEPENDENCY ${VERSION_FILE}
        DEPENDS ${CMAKE_SOURCE_DIR}/.git/HEAD
    )

endfunction()
