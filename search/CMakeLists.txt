CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT(SMARTCOOK)

ADD_EXECUTABLE(
    smartcook

    content_system.cpp
    document.cpp
    index.cpp
    query.cpp

    main.cpp)
