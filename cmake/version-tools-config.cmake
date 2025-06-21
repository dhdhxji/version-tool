function(template_version VERSION_FILE TEMPLATE OUTPUT)

    add_custom_command(
        OUTPUT ${OUTPUT}
        COMMAND python3 ${CMAKE_CURRENT_LIST_DIR}/tools/version_tools.py 
                        ${VERSION_FILE}
                        ${TEMPLATE}
                        ${OUTPUT}
        MAIN_DEPENDENCY ${VERSION_FILE}
        DEPENDS ${CMAKE_SOURCE_DIR}/.git/HEAD
    )

        # WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
endfunction()
