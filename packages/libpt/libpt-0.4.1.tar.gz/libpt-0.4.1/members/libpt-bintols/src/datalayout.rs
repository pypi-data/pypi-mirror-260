//* # See what's behind the datatypes of Rust
//*
//* This Crate shows off how datatypes of rust are stored in memory.

// reexport macros
pub use crate::investigate_memory_layout;

/// ## Investigate the internal representation of variables
///
/// Takes 1. the Type and 2. a [`Vec`] of items (of that datatype).
#[macro_export]
macro_rules! investigate_memory_layout {
    ($t:ty, $v:tt) => {
        println!("Type:\t{}", std::any::type_name::<$t>());
        println!("\talign:\t{:?} B", std::mem::align_of::<$t>());
        println!("\tID:\t{:?}\n", std::any::TypeId::of::<$t>());
        println!("\tItems:");
        unsafe {
            for (index, item) in $v.iter().enumerate() {
                let pointer = item as *const $t;
                let mut memory: [u8; std::mem::size_of::<$t>()] = std::mem::transmute(item.clone());
                memory.reverse();
                println!(
                    "\
                    \t{index:02x}\titem:\t\t{item:?}\n\
                    \t\tpointer:   \t{:X?}\n\
                    \t\talign:     \t{}\n\
                    \t\tsize:      \t{}\n\
                    \t\tmemory:    \t{:X?}\n\
                    \t\tbin mem:   \t{}\n\
                    \t\tnote:      \tmemory order reversed\n\
                    ",
                    pointer,
                    display::byte_bit_display(std::mem::align_of_val(item)),
                    display::byte_bit_display(memory.len()),
                    memory,
                    display::bytes_to_bin(&memory)
                );
            }
        }
    };
}
