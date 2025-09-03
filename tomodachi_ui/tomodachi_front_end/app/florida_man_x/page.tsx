'use client';

import { useEffect, useState } from 'react';

export default function FloridaManX(){
    const [result, setResult] = useState<number | null>(null);
    useEffect(() => {
        (async () => {
        const response = await fetch('/florida_man.wasm');
        const buffer = await response.arrayBuffer();
        const wasm = await WebAssembly.instantiate(buffer, {});
        const value = (wasm.instance.exports.get_number as CallableFunction)();
        setResult(value);
        })();
    }, []);

    return (
        <section className='flex justify-center items-center flex-col gap-5'>
            <h1 className='text-blue-800'>Florida Max X</h1>
            <p>WASM result: {result !== null ? result : 'Loading...'}</p>
        </section>
    );
}