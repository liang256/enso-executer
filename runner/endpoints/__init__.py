from service_layer import services


def case_multiple_disciplines_flow():
    instructions = [
        ("open_houdini_file", {"file": "cloth/sim/template.hip"}),
        ("cloth_prequire_process", {"asset_version_uri": "acp-version-uri"}),
        ("release_and_post_publish", {}),
        ("open_houdini_file", {"file": "fur/sim/template.hip"}),
        ("fur_prequire_process", {"asset_version_uri": "acp-version-uri"}),
        ("release", {}),
    ]
    services.execute(instructions)
