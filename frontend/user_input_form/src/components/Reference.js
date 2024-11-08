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
            // localhost:8000
            const response = await axios.post('http://106.14.184.241/postdata/upload/', formData);
            if (response.status === 201) {  // 假设状态码 200 表示上传成功
                setUploadStatus('Upload successful!');
                fetchUploadedFiles();
                // 上传成功后清空输入内容
                textInputRef.current.value = "";  // 清空文本输入域
                fileInputRef.current.value = "";  // 清空文件输入域
                // urlInputRef.current.value= "";
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
            // localhost:8000
            await axios.delete('http://106.14.184.241/postdata/upload/');
            setUploadedFiles([]);
            alert('参考资料已清空！');
        } catch (error) {
            console.log('Error:', error);
        }
    };

    const fetchUploadedFiles = async () => {
        try {
            // localhost:8000
            const response = await axios.get('http://106.14.184.241/postdata/upload/');
            setUploadedFiles(response.data.uploaded_files);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="reference">
            {/* <h2>Reference</h2> */}
            {/* <h3>You can upload your references here</h3> */}
            <form className="uploadForm" encType="multipart/form-data" onSubmit={handleSubmit}>
                <div className="fields">
                    <label id="reference_text" htmlFor="text">文本</label>
                    <textarea 
                        ref={textInputRef} 
                        id="text" 
                        name="text" 
                        // placeholder="请你输入参考文本"
                        >
                    </textarea>
                </div>
                <div className="fields">
                    <label htmlFor="file"> 文件 （PDF，DOC，TEXT）</label>
                    <input
                        ref={fileInputRef}
                        type="file" 
                        id="single_file" 
                        name="single_file" 
                        accept=".pdf, .txt, .docx, .doc" 
                    />
                </div>
                <div className="fields">
                    <label htmlFor="website">网页</label>
                    <input
                        url={urlInputRef}
                        type="url" 
                        id="url" 
                        name="url" 
                        // placeholder="请你输入网页链接"
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
                <button type="submit" id="submitUpload">上传</button>
            </form>
            {/* <div id="uploadStatus" className="text-center mt-4">{uploadStatus}</div> */}
            <h3>已上传的文件</h3>
            <div className="uploadedFilesList">
                <ul className="list-inside">
                    {uploadedFiles.map((file, index) => <li key={index}>{file}</li>)}
                </ul>
            </div>
            <button onClick={handleDeleteAllFiles}>清空</button>
        </div>
    );
}

export default Reference;