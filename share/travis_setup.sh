#!/bin/bash
set -evx

mkdir ~/.trivechaincore

# safety check
if [ ! -f ~/.trivechaincore/.trivechain.conf ]; then
  cp share/trivechain.conf.example ~/.trivechain/trivechain.conf
fi
