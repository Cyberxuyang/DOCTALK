"use client";

import FileUploader from "@/components/FileUploader";
import * as React from "react";

import { MoveRight } from "lucide-react";

export default function IndexPage() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <h1 className="text-5xl font-bold">DOCTALK</h1>
        <ol className="list-inside list-decimal text-sm text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
          <p className="text-xl text-gray-500">
            Discuss Research Papers Locally with LLM and RAG
          </p>
        </ol>
        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <FileUploader />
          <a
            className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
            href="https://github.com/Cyberxuyang/DOCTALK/tree/main"
            target="_blank"
            rel="noopener noreferrer"
          >
            Github
            <MoveRight size={15} />
          </a>
        </div>
      </main>
    </div>
  );
}
