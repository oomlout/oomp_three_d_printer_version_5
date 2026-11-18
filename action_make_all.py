"""Build the photographic catalogue. Legacy CAD stages are explicit options."""

def main(**kwargs):
    kwargs["run_oomp_populate"] = True

    kwargs["run_oomp"] = True

    kwargs["run_action"] = True
    #kwargs["run_action"] = False

    # True: native recipe; False: off; "working_scad": share SCAD definitions.
    kwargs.setdefault("run_solidcraft", False)
    kwargs.setdefault("run_scad", bool(kwargs["run_solidcraft"]))

    kwargs["run_svg"] = True

    kwargs.setdefault("generate_stl", kwargs["run_scad"])

    # Rebuild native CAD and all selected exports from the recipe every run.
    kwargs["export_extras"] = kwargs.get("export_extras", True)  # STEP and PNG previews.
    kwargs["export_stl"] = kwargs.get("export_stl", True)
    kwargs["verify_solidcraft"] = kwargs.get("verify_solidcraft", False)

    import working
    working.run(**kwargs)

if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
