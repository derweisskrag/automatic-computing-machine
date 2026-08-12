using System.ComponentModel;
using System.Globalization;
using System.Runtime.CompilerServices;

namespace App.Machine.Types {
    public class Result<T, E>
        where E : System.Exception
    {
        private Result() {}

        public sealed class Ok :  Result<T, E> {
            public T Value { get; }

            public Ok(T value) => Value = value;
        }

        public sealed class Err : Result<T, E> {
            public new E Error { get; }

            public Err(E error) => Error = error;
        }


        public static Result<T, E> Success(T value) => new Ok(value);
        public static Result<T, E> Error(E error) => new Err(error);
    }
}