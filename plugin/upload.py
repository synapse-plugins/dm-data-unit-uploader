"""Upload action for dm-data-unit-uploader-v2."""

from __future__ import annotations

from synapse_sdk.plugins.actions.upload import DefaultUploadAction, UploadParams


class UploadAction(DefaultUploadAction[UploadParams]):
    """Upload action for dm-data-unit-uploader-v2.

    This action handles data upload from external sources using an 8-step workflow:
    1. Initialize - Setup storage and paths
    2. Process Metadata - Load Excel metadata (optional)
    3. Analyze Collection - Load file specifications
    4. Organize Files - Group files by stem
    5. Validate Files - Validate against specs
    6. Upload Files - Upload to storage
    7. Generate Data Units - Create data units
    8. Cleanup - Final cleanup

    Supports both single-path and multi-path modes for flexible file organization.

    Single Path Mode (use_single_path=True, DEFAULT):
        All file specifications share one base path.
        Example:
            params = {
                'name': 'Standard Upload',
                'path': '/data/experiment_1',
                'storage': 1,
                'data_collection': 5,
            }

    Multi-Path Mode (use_single_path=False):
        Each file specification has its own path.
        Example:
            params = {
                'name': 'Multi-Source Upload',
                'use_single_path': False,
                'assets': {
                    'image_1': {'path': '/sensors/camera', 'is_recursive': True},
                    'pcd_1': {'path': '/sensors/lidar', 'is_recursive': False},
                },
                'storage': 1,
                'data_collection': 5,
            }

    Customization:
        Override setup_steps() to customize the workflow:

        def setup_steps(self, registry: StepRegistry[UploadContext]) -> None:
            # Call parent to register default steps
            super().setup_steps(registry)
            # Or register custom steps instead
    """

    action_name = 'upload'
    params_model = UploadParams

    def get_allowed_extensions(self) -> dict[str, list[str]] | None:
        """Allow only MP4 for video, default extensions for other types."""
        return {
            'image': ['.jpg', '.jpeg', '.png'],
            'video': ['.mp4'],  # Default: .mp4, .avi, .mov, .mkv, .webm, .flv, .wmv
            'audio': ['.mp3', '.wav'],
            'text': ['.txt', '.html', '.csv'],
            'pcd': ['.pcd'],
            'data': ['.bin', '.json', '.fbx', '.xml'],
        }
