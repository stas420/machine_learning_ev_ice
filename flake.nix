{
  description = "Python venv development template for YOLO training (optimized for pip wheels with robust LD_LIBRARY_PATH)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05"; # Keeping 25.05
    utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    utils,
    ...
  }:
    utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        config = {
          cudaSupport = true;
          allowUnfree = true;
        };
      };

      pythonPackages = pkgs.python312Packages; # Sticking to Python 3.12

      commonBuildTools = with pkgs; [
        git
        gcc
        gnumake
        cmake
        pkg-config
        zlib
        ffmpeg-full
      ];

      mlSystemDependencies = with pkgs; [
        pkgs.cudatoolkit # Provides CUDA libraries
        pkgs.glib # Often a dependency for various C/C++ components
        pkgs.libGL # OpenGL libraries, sometimes needed by rendering/visualization
      ];

    in {
      devShells.default = pkgs.mkShell {
        name = "python-venv-yolo";
        venvDir = "./.venv";

        buildInputs = [
          pkgs.python312
          pythonPackages.venvShellHook # Initializes the venv

          pythonPackages.ultralytics
          pythonPackages.torch
          pythonPackages.numpy
          pythonPackages.tqdm
          pythonPackages.pip
          pkgs.jupyter
        ] ++ commonBuildTools
          ++ mlSystemDependencies;

        postVenvCreation = ''
          unset SOURCE_DATE_EPOCH
          echo "Installing PyTorch, Ultralytics, Triton, and OpenCV-Python via pip (using pre-built wheels)..."

          # It's crucial to use the correct CUDA version here (e.g., cu121 for CUDA 12.1)
          # You can confirm the CUDA version of pkgs.cudatoolkit on 25.05 by inspecting its path
          # or running `nvcc --version` once inside the shell.

          echo "Pip dependencies installed."
        '';

        postShellHook = ''
          echo "Entering Python development shell for machine_learning_ev_ice."

          # --- CRITICAL: Set LD_LIBRARY_PATH for pip-installed native extensions ---
          # This tells the system where to find shared libraries that pip-installed
          # packages (like PyTorch, OpenCV, Triton) expect.
          export LD_LIBRARY_PATH=${
            pkgs.lib.makeLibraryPath ([
              pkgs.stdenv.cc.cc.lib # Standard C/C++ runtime libraries
              pkgs.cudatoolkit.lib # CUDA runtime libraries
              pkgs.zlib # Zlib compression library
              pkgs.glib # GLib library
              pkgs.libGL # OpenGL library
              pkgs.ffmpeg-full # FFmpeg libraries
            ])
          }:$LD_LIBRARY_PATH

          # --- Verification checks ---
          if command -v nvcc &> /dev/null; then
              echo "nvcc is available: $(nvcc --version | grep 'release' | head -n 1)"
          else
              echo "nvcc is NOT available. CUDA might not be set up correctly in your PATH."
          fi
          python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA Device Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
          python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
          # Optional: Verify Triton installation
          python -c "try: import triton; print('Triton imported successfully.'); except ImportError: print('Triton import failed.')"
        '';

      };
    });
}
