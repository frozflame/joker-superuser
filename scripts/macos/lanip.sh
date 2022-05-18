#!/usr/bin/env bash

ifconfig | perl -lne 's/\s*inet (\d+\.\d+\.\d+.\d+).*/$1/ or next; print' | grep -v 127.0.0.1
