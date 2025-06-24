set(VERSION_TOOL_DIR "${CMAKE_CURRENT_LIST_DIR}/..")

function(update_git_state_file TARGET GIT_EXEC GIT_REPO_PATH)

    add_custom_target(
        ${TARGET}_git_state_target
        BYPRODUCTS ${TARGET}_git_state
        COMMAND python3 ${VERSION_TOOL_DIR}/version_tools.py update-git-state-file
                        --git-exec ${GIT_EXEC}
                        --repo-path ${GIT_REPO_PATH}
                        --git-state-path ${TARGET}_git_state
    )

endfunction()

function(template_version VERSION_FILE TEMPLATE OUTPUT GIT_REPO_PATH)

    update_git_state_file(${OUTPUT} git ${GIT_REPO_PATH})
    string(REPLACE "/" "_" output_target ${OUTPUT})
    string(REPLACE ":" "_" output_target ${output_target})

    add_custom_command(
        OUTPUT ${OUTPUT}
        COMMAND python3 ${VERSION_TOOL_DIR}/version_tools.py template
                        --version-file ${VERSION_FILE}
                        --template ${TEMPLATE}
                        --output ${OUTPUT}
                        --git-exec git
                        --repo-path ${GIT_REPO_PATH}
        DEPENDS ${VERSION_FILE} ${TEMPLATE} ${OUTPUT}_git_state_target ${OUTPUT}_git_state
    )

endfunction()

