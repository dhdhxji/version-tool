cmake_minimum_required(VERSION "3.16")

project(ababagalamaga)

set(version-tools_DIR "${PROJECT_SOURCE_DIR}/cmake/")

find_package(version-tools REQUIRED)
template_version(${CMAKE_CURRENT_SOURCE_DIR}/version.json ${CMAKE_CURRENT_SOURCE_DIR}/version.h.template version.h)

add_executable(app main.c version.h)

