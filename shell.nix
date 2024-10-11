let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import <nixpkgs> { };
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs:
      with python-pkgs; [
        # select Python packages here
        ontospy
        openai
        polar
        pydantic
        python-dotenv
        scikit-learn
        torch
        tqdm
        transformers
        black
        isort
        pyright
        flake8
      ]))
  ];
}
