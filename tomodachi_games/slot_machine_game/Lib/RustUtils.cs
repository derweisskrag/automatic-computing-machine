using System.Runtime.InteropServices;

namespace App.Machine.Lib {
    public class RustUtils {
        [DllImport(".\\Lib\\rust_sqlite_lib.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern void insert_person(int id, IntPtr name);

        [DllImport(".\\Lib\\rust_sqlite_lib.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern IntPtr read_user_db_query();

        [DllImport(".\\Lib\\rust_sqlite_lib.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern void create_person_database();

        [DllImport(".\\Lib\\rust_sqlite_lib.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern void hello_from_rust();

        [DllImport(".\\Lib\\rust_sqlite_lib.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern bool check_result(string x, string y, string z);

        [DllImport(".\\Lib\\rust_sqlite_lib.dll", CallingConvention = CallingConvention.Cdecl)]
        public static extern float calculate_new_currency(decimal amount, decimal ToRate, decimal FromRate);
    }
}