with import <nixpkgs> {}; {
  pyEnv = stdenv.mkDerivation {
    name = "caudexer";
    buildInputs = [ python35
                    python35Packages.virtualenv
		    python35Packages.tox
		    postgresql
                    libxml2
                    libxslt
                    readline ];
    LD_LIBRARY_PATH="${libxml2}/lib:${libxslt}/lib";
    shellHook = ''
      [[ -d venv ]] || virtualenv venv
      venv/bin/pip install -r dexer/requirements.txt
    '';
  };
}
