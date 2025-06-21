function(template_version)

    add_custom_command(
        OUTPUT version.h
        COMMAND python3 ${CMAKE_CURRENT_LIST_DIR}/tools/version_tools.py
        DEPENDS ${CMAKE_SOURCE_DIR}/version.json ${CMAKE_SOURCE_DIR}/.git/HEAD
    )

endfunction()
