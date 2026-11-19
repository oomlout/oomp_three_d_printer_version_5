"""Run catalogue actions without desktop automation."""
def main(**kwargs):
    labels_already_built = kwargs.get("run_svg", False)

    if not labels_already_built:
        import working_svg
        working_svg.main(**kwargs)
    import working_images
    working_images.main(**kwargs)
    import action_documentation
    action_documentation.main(**kwargs)


if __name__ == "__main__":
    main()
