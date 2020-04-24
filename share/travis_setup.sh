#!/bin/bash
set -evx

mkdir ~/.trivechain

# safety check
if [ ! -f ~/.trivechain/.trivechain.conf ]; then
  cp share/trivechain.conf.example ~/.trivechain/trivechain.conf
fi
