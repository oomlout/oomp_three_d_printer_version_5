import copy
from time import monotonic

from build_progress import stage

def main(**kwargs):
    run_oomp_populate = kwargs.get("run_oomp_populate", True)
    #run_oomp_populate = False
    kwargs["run_oomp_populate"] = run_oomp_populate

    run_oomp = kwargs.get("run_oomp", True)
    #run_oomp = False
    kwargs["run_oomp"] = run_oomp

    run_scad = kwargs.get("run_scad", False)
    #run_scad = False
    kwargs["run_scad"] = run_scad

    run_svg = kwargs.get("run_svg", True)
    kwargs["run_svg"] = run_svg

    run_action = kwargs.get("run_action", True)
    #run_action = False
    kwargs["run_action"] = run_action

    generate_stl = kwargs.get("generate_stl", False)
    #generate_stl = True
    kwargs["generate_stl"] = generate_stl

    run(**kwargs)

def run(**kwargs):
    start = monotonic()
    print(f"[build] Catalogue filter {kwargs.get('filter') or '*'}", flush=True)
    import working_cad
    selected_solidcraft = working_cad.solidcraft_mode(kwargs.get("run_solidcraft", False))
    native_context = dict(kwargs.pop("solidcraft_context", None) or {})
    if selected_solidcraft == "working_scad":
        native_context["recipe_source"] = "working_scad"
    native_context["export_extras"] = kwargs.pop("export_extras", native_context.get("export_extras", False))
    native_context["export_stl"] = kwargs.pop("export_stl", native_context.get("export_stl", False))
    native_context["verify_solidcraft"] = kwargs.pop("verify_solidcraft", native_context.get("verify_solidcraft", False))


    kwargs_2 = copy.deepcopy(kwargs)
    #pop run and generate variables from kwargs
    pop_values = ["run_oomp_populate", "run_oomp", "run_scad", "run_action", "generate_stl", "run_svg", "run_solidcraft", "solidcraft_context"]
    for key in pop_values:
        kwargs_2.pop(key, None)


    if kwargs.get("run_oomp_populate", False):
        stage("population", "working_oomp_populate", **kwargs_2)

    if kwargs.get("run_oomp", False):
        oomp_kwargs = copy.deepcopy(kwargs_2)
        if kwargs.get("run_solidcraft", False):
            oomp_kwargs["wait_for_completion"] = True
        stage("canonical records", "working_oomp", **oomp_kwargs)

    if kwargs.get("run_scad", False):        
        kwargs2 = copy.deepcopy(kwargs_2)
        if kwargs.get("generate_stl", False):
            kwargs2["typ"] = "all"
        stage("SCAD", "working_scad", **kwargs2)

    #add run_svg
    if kwargs.get("run_svg", False):        
        stage("SVG and PDF labels", "working_svg", **kwargs_2)


    if kwargs.get("run_action", False):
        stage("catalogue actions", "working_action", **kwargs)

    # Opt-in native route runs after legacy actions/OOMP regeneration.
    if kwargs.get("run_solidcraft", False):
        stage("SolidCraft", "working_solidcraft", solidcraft_context=native_context)

    print(f"[build] Complete in {monotonic() - start:.1f}s", flush=True)




if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
