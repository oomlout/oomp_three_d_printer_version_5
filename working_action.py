"""Run catalogue actions without desktop automation."""
from build_progress import stage


def main(**kwargs):
    labels_already_built = kwargs.get("run_svg", False)

    if not labels_already_built:
        stage("SVG and PDF labels", "working_svg", **kwargs)
    stage("credited photographs", "working_images", **kwargs)
    stage("navigation and part pages", "action_documentation", **kwargs)


if __name__ == "__main__":
    main()
