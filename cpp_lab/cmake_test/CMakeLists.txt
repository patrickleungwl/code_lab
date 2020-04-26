cmake_minimum_required(VERSION 3.5)

project(cmake_test)

add_executable(${PROJECT_NAME} test01.cpp)

install(TARGETS ${PROJECT_NAME} DESTINATION /tmp)
install(FILES test01.cpp DESTINATION /tmp/src)


