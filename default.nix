with import <nixpkgs> {}; {
  pyEnv = stdenv.mkDerivation {
    name = "caudexer";
    buildInputs = [ python35
                    python35Packages.virtualenv
                    python35Packages.tox
                    python35Packages.sqlite3
#                   python27Packages.virtualenv
                    postgresql
                    libxml2
                    libxslt
                    readline 
                    autoconf ];
    LD_LIBRARY_PATH="${libxml2}/lib:${libxslt}/lib";
    shellHook = ''
      [[ -d venv ]] || virtualenv-3.5 venv
      venv/bin/pip3 install -r dexer/requirements.txt
      [[ -d fabric ]] || virtualenv-2.7 fabric
      fabric/bin/pip install fabric
    '';
  };
}
