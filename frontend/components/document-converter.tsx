"use client"

import type React from "react"
import { useState, useRef } from "react"
import axios from "axios" 
import { FileUp, Download, RotateCcw, Loader2, CheckCircle, ImageIcon, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

// Possible states for the converter
type ConverterState = "idle" | "processing" | "success" | "error"

// Main Document Converter Component
export function DocumentConverter() {
  const [state, setState] = useState<ConverterState>("idle")
  const [file, setFile] = useState<File | null>(null)
  const [downloadUrl, setDownloadUrl] = useState<string>("")
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }



  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    const droppedFiles = e.dataTransfer.files
    if (droppedFiles && droppedFiles.length > 0) {
      const selectedFile = droppedFiles[0]
      if (isValidFile(selectedFile)) setFile(selectedFile)
    }
  }
// Validate file type
  const isValidFile = (file: File): boolean => {
    const validTypes = ["application/pdf", "image/jpeg", "image/png", "image/webp", "image/gif"]
    return validTypes.includes(file.type)
  }
// Handle file selection via input
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0]
      if (isValidFile(selectedFile)) setFile(selectedFile)
    }
  }

// Handle file conversion
  const handleConvert = async () => {
    if (!file) return

    setState("processing")
    const formData = new FormData()
    formData.append("file", file)

    // Send file to backend for conversion
    try {
      const response = await axios.post("http://127.0.0.1:8000/convert", formData, {
        responseType: "blob", 
      })

      // Create a temporary download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      setDownloadUrl(url)
      setState("success")
    } catch (error) {
      console.error("Error converting file:", error)
      setState("error")
    }
  }

// Handle converting another file
  const handleConvertAnother = () => {
    setState("idle")
    setFile(null)
    setDownloadUrl("")
    if (fileInputRef.current) fileInputRef.current.value = ""
  }

  // Handle file download
  const handleDownload = () => {
    if (!downloadUrl) return
    const link = document.createElement("a")
    link.href = downloadUrl
    link.download = `converted_${file?.name || "document"}.docx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }


  // Processing state UI
  if (state === "processing") {
    return (
      <div className="flex flex-col items-center justify-center gap-8 py-12">
        <Loader2 className="w-16 h-16 text-blue-600 animate-spin" />
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-900">Processing...</h2>
          <p className="text-gray-500 text-sm mt-2">Converting {file?.name} to Word format</p>
        </div>
      </div>
    )
  }


  // Success state UI
  if (state === "success") {
    return (
      <Card className="w-full max-w-md bg-white rounded-2xl border border-gray-200 shadow-lg mx-auto">
        <div className="p-8 flex flex-col items-center gap-6">
          <div className="flex items-center justify-center w-16 h-16 rounded-full bg-emerald-50">
            <CheckCircle className="w-8 h-8 text-emerald-600" />
          </div>
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-900">Conversion Complete!</h2>
            <p className="text-gray-500 text-sm mt-2">Your file is ready to download</p>
          </div>
          <div className="w-full bg-gray-50 rounded-xl p-4 border border-gray-200">
            <p className="text-sm font-medium text-gray-700 truncate">{file?.name}</p>
            <p className="text-xs text-gray-500 mt-1">{(file ? file.size / 1024 : 0).toFixed(1)} KB</p>
          </div>
          <div className="w-full flex gap-3">
            <Button onClick={handleDownload} className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium h-12">
              <Download className="w-4 h-4 mr-2" /> Download
            </Button>
            <Button onClick={handleConvertAnother} variant="outline" className="flex-1 border-gray-300 h-12">
              <RotateCcw className="w-4 h-4 mr-2" /> New File
            </Button>
          </div>
        </div>
      </Card>
    )
  }


  // Error state UI
  if (state === "error") {
    return (
      <div className="flex flex-col items-center justify-center gap-6 py-12">
        <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center">
          <AlertCircle className="w-8 h-8 text-red-600" />
        </div>
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-900">Conversion Failed</h2>
          <p className="text-gray-500 mt-2">Something went wrong. Is the backend running?</p>
        </div>
        <Button onClick={handleConvertAnother} variant="outline">Try Again</Button>
      </div>
    )
  }


  // Idle state UI
  return (
    <div className="w-full max-w-3xl mx-auto px-6">
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-900 tracking-tight">Sinhala OCR Converter</h1>
        <p className="text-gray-600 text-lg mt-3 font-light">Convert PDF and images to Word documents instantly</p>
      </div>

      <div className="flex flex-col items-center gap-10">
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`w-full px-8 py-20 rounded-2xl border-2 border-dashed transition-all cursor-pointer shadow-sm ${
            dragActive ? "border-blue-600 bg-blue-50" : "border-gray-300 bg-white hover:border-blue-400 hover:bg-blue-50"
          }`}
        >
          <input ref={fileInputRef} type="file" accept=".pdf,image/jpeg,image/png,image/webp,image/gif" onChange={handleFileSelect} className="hidden" />
          
          <div className="flex flex-col items-center gap-6">
            <div className={`p-5 rounded-full transition-all ${dragActive ? "bg-blue-600 text-white" : "bg-blue-100 text-blue-600"}`}>
              {file ? <FileUp className="w-8 h-8" /> : <ImageIcon className="w-8 h-8" />}
            </div>
            <div className="text-center">
              <p className="text-xl font-semibold text-gray-900">{file ? file.name : "Drag and drop your file"}</p>
              {!file && <p className="text-gray-600 mt-2 text-base font-light">or click to browse</p>}
              {!file && <p className="text-sm text-gray-500 mt-1">PDF, JPG, PNG, WebP, or GIF</p>}
              {file && <p className="text-sm text-gray-500 mt-2">{(file.size / 1024).toFixed(1)} KB</p>}
            </div>
          </div>
        </div>

        <Button onClick={handleConvert} disabled={!file} className={`px-12 py-3 rounded-lg font-semibold text-base transition-all ${file ? "bg-blue-600 hover:bg-blue-700 text-white shadow-md" : "bg-gray-200 text-gray-500 cursor-not-allowed"}`}>
          Convert
        </Button>
        
        {file && (
          <button onClick={() => { setFile(null); if (fileInputRef.current) fileInputRef.current.value = ""; }} className="text-sm text-gray-500 hover:text-blue-600 transition-colors font-light">
            Clear selection
          </button>
        )}
      </div>
    </div>
  )
}