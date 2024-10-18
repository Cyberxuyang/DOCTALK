"use client";

import Image from "next/image";
import { Button } from "./ui/button";
import { useDropzone } from "react-dropzone";
import { useRouter } from "next/navigation";
import { useState, useCallback } from "react";
import React, { useContext } from "react";
import { MyContext } from "@/app/MyContext";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function FileUploader() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null); // 只存储一个文件
  // const [fileUrl, setFileUrl] = useState<string | null>(null); // 用来存储文件的 URL
  const { setPdfUrl } = useContext(MyContext);
  // 当文件被上传（拖拽或点击选择）时调用
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const selectedFile = acceptedFiles[0]; // 只处理第一个文件
    setFile(selectedFile); // 更新 file 变量
    const url = URL.createObjectURL(selectedFile); // 创建文件的 URL
    setPdfUrl(url); // 更新 fileUrl 变量
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, // 当文件上传时调用
    accept: { "application/pdf": [] }, // 只接受 PDF 文件
    multiple: false, // 确保只上传一个文件
  });

  return (
    <Dialog>
      <DialogTrigger asChild>
        <a
          className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            className="dark:invert"
            src="https://nextjs.org/icons/vercel.svg"
            alt="Vercel logomark"
            width={20}
            height={20}
          />
          UPload File
        </a>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[800px] sm:max-h-[800px]">
        <DialogHeader>
          <DialogTitle className="text-center">
            Upload your PDF file
          </DialogTitle>
          <DialogDescription className="text-center">
            Drag and drop or click to upload
          </DialogDescription>
        </DialogHeader>

        {/* 文件拖拽/点击上传区域 */}
        <div
          {...getRootProps()}
          className={`border-2 border-dashed p-6 text-center cursor-pointer rounded-lg ${
            isDragActive ? "border-blue-500 bg-blue-100" : "border-gray-400"
          }`}
        >
          <input {...getInputProps()} />
          <p className="text-gray-500">
            {isDragActive
              ? "Drop the PDF file here..."
              : "Drag & drop PDF file here, or click to select file"}
          </p>
        </div>

        {/* 显示选择的文件 */}
        {file && (
          <ul className="mt-4 list-disc list-inside text-sm text-gray-700">
            <li>{file.name}</li>
          </ul>
        )}

        <Button
          className="mt-4"
          onClick={() => router.push("/pdfWithChat")}
          disabled={!file}
        >
          Upload
        </Button>
      </DialogContent>
    </Dialog>
  );
}
