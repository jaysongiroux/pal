if(${CMAKE_GENERATOR} MATCHES "Visual Studio")
    enable_language(ASM_MASM)

    add_library(libpal 
	    control_registers_x64.asm
	    cpuid_x64.asm
	    extended_control_registers_x64.asm
	    rdmsr_x64.asm
	    vmread_x64.asm
	    vmwrite_x64.asm
	    wrmsr_x64.asm
    )
    set_target_properties(libpal PROPERTIES OUTPUT_NAME pal)
    target_include_directories(libpal PUBLIC ${CMAKE_CURRENT_LIST_DIR})
endif()
