class ArmInfo:
    nop_bytes = b"\x00\xf0\x20\xe3"  # TODO: thumb
    nop_size = 4
    jmp_asm = "b {dst}"
    jmp_size = 4
    call_asm = "bl {dst}"
    pc_reg_names = ["pc", "r15", "ip"]
    save_context_asm = """
        push {r0-r11}
    """
    restore_context_asm = """
        pop {r0-r11}
    """
