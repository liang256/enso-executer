def test_input_a_single_acp_output_instructions():
    acp_av_uri = "dummp-acp-asset-version-uri"
    expected_instructions = [
        ("open_houdini_file", {"file": "path/to/file.hip"}),
        ("update_acp", {"asset_version_uri": "acp-version-uri"}),
        ("release", {}),
    ]
    res = determine_instructions([acp_av_uri])

    assert res == expected_instructions


def test_input_multiple_acps_output_instructions():
    cloth_acp_uri = "cloth_acp_uri"
    fur_acp_uri = "fur_acp_uri"
    expected_instructions = [
        ("open_houdini_file", {"file": "cloth/sim/template.hip"}),
        ("cloth_prequire_process", {"asset_version_uri": "acp-version-uri"}),
        ("release_and_post_publish", {}),
        ("open_houdini_file", {"file": "fur/sim/template.hip"}),
        ("fur_prequire_process", {"asset_version_uri": "acp-version-uri"}),
        ("release", {}),
    ]
    res = determine_instructions([cloth_acp_uri, fur_acp_uri])

    assert res == expected_instructions


def test_input_a_root_and_a_context_output_instructions():
    root_uri = "root-uri"
    cxt_uri = "context-uri"
    expected_instructions = [
        ("open_houdini_file", {"file": "path/to/root/template.hip"}),
        ("prequire_process", {"context-uri": "context-uri"}),
        ("release", {}),
    ]
    res = determine_instructions([root_uri, cxt_uri])

    assert res == expected_instructions


def test_single_discipline_flow():
    instructions = [
        ("open_houdini_file", {"file": "path/to/file.hip"}),
        ("update_acp", {"asset_version_uri": "acp-version-uri"}),
        ("release", {}),
    ]


def test_multiple_disciplines_flow():
    instructions = [
        ("open_houdini_file", {"file": "cloth/sim/template.hip"}),
        ("cloth_prequire_process", {"asset_version_uri": "acp-version-uri"}),
        ("release_and_post_publish", {}),
        ("open_houdini_file", {"file": "fur/sim/template.hip"}),
        ("fur_prequire_process", {"asset_version_uri": "acp-version-uri"}),
        ("release", {}),
    ]

    for script_name, arg in instructions:
        # assert get_script function return correct scripts
        # each script has its own execute tests
        get_script(script_name).execute(arg)


def test_execute_two_instruction_sets_parallelly():
    set1 = [("print", {"text": "execute instruction set 1."})]
    set2 = [("print", {"text": "execute instruction set 2."})]
    set_root = [
        ("parallel_execute_instruction_sets", {"sets": [set1, set2]}),
    ]
