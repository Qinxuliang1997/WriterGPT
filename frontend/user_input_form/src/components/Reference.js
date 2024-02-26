import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function Reference() {
    const [uploadStatus, setUploadStatus] = useState('');
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const  user_name = localStorage.getItem('user_name');
    const textInputRef = useRef(null);  // 添加一个引用来访问文本输入域
    const fileInputRef = useRef(null);  // 添加一个引用来访问文件输入域
    const urlInputRef = useRef(null);
    
    useEffect(() => {
        fetchUploadedFiles();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setUploadStatus('Uploading...');
        const formData = new FormData(e.target);
        try {
            const response = await axios.post('http://localhost:8000/postdata/upload/', formData);
            if (response.status === 201) {  // 假设状态码 200 表示上传成功
                setUploadStatus('Upload successful!');
                fetchUploadedFiles();
                // 上传成功后清空输入内容
                textInputRef.current.value = "";  // 清空文本输入域
                fileInputRef.current.value = "";  // 清空文件输入域
                urlInputRef.current.value= "";
            } else {
                // 处理非 200 响应状态码
                setUploadStatus('Upload failed, please try again.');
            }
        } catch (error) {
            setUploadStatus('Error occurred!');
            console.error('Error:', error);
        }
    };

    const handleDeleteAllFiles = async () => {
        try {
            await axios.delete('http://localhost:8000/postdata/upload/');
            setUploadedFiles([]);
            alert('All files deleted');
        } catch (error) {
            console.log('Error:', error);
        }
    };

    const fetchUploadedFiles = async () => {
        try {
            const response = await axios.get('http://localhost:8000/postdata/upload/');
            setUploadedFiles(response.data.uploaded_files);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="info">
            {/* <h2>Reference</h2> */}
            {/* <h3>You can upload your references here</h3> */}
            <form className="uploadForm" encType="multipart/form-data" onSubmit={handleSubmit}>
                <div className="fields">
                    <label id="reference_text" htmlFor="text">Text:</label>
                    <textarea 
                        ref={textInputRef} 
                        id="text" 
                        name="text" 
                        placeholder="Text">
                    </textarea>
                </div>
                <div className="fields">
                    <label htmlFor="file"> File (pdf,txt,doc):</label>
                    <input
                        ref={fileInputRef}
                        type="file" 
                        id="single_file" 
                        name="single_file" 
                        accept=".pdf, .txt, .docx" 
                    />
                </div>
                <div className="fields">
                    <label htmlFor="website">Website URL:</label>
                    <input
                        url={urlInputRef}
                        type="url" 
                        id="url" 
                        name="url" 
                        placeholder="Website URL"
                    />
                </div>
                {/* <div>
                    <label htmlFor="folder">Folder:</label>
                    <input
                        type="file" 
                        id="folder" 
                        name="folder"
                        webkitdirectory
                        directory 
                        multiple
                        />
                </div> */}
                <button type="submit" id="submitUpload">Upload</button>
            </form>
            {/* <div id="uploadStatus" className="text-center mt-4">{uploadStatus}</div> */}
            <h3>Uploaded Files:</h3>
            <div id="uploadedFilesList" className="mt-4">
                <ul id="filesList" className="list-disc list-inside">
                    {uploadedFiles.map((file, index) => <li key={index}>{file}</li>)}
                </ul>
            </div>
            <button onClick={handleDeleteAllFiles}>Delete All Files</button>
        </div>
    );
}

export default Reference;