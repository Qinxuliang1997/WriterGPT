import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useDispatch, useSelector } from 'react-redux';
import { back, next } from '../features/pages';
import { info } from '../features/description';
import { useNavigate } from 'react-router-dom';
import apiClient, { setupAxiosInterceptors } from '../interceptors/axioss';

function Reference() {
    const [uploadStatus, setUploadStatus] = useState('');
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const description = useSelector((e) => e.description.value);
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user_name = localStorage.getItem('user_name');
    const textInputRef = useRef(null);
    const fileInputRef = useRef(null);
    const urlInputRef = useRef(null);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        fetchUploadedFiles();
    }, []);

    useEffect(() => {
        setupAxiosInterceptors(navigate, (message) => {
          setErrorMessage(message);
        });
      }, [navigate]);

    const GenerateClick = async () => {
        if (isLoading) return;
        setIsLoading(true);
        setProgress(0);
        setErrorMessage('')
        const desiredTimeInSeconds = 10; //todo
        const updatesPerSecond = 10;
        const step = 100 / (desiredTimeInSeconds * updatesPerSecond); 
        let interval = setInterval(() => {
          setProgress(prevProgress => {
            if (prevProgress >= 100) {
              clearInterval(interval);
              return 100;
            }
            return prevProgress + step;
          });
        }, 1000 / updatesPerSecond);
        try {
            const response = await apiClient.post('http://106.14.184.241/api/outline/', {description, manner: 'general_writting' }, {
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            console.log('成功发送：', response.data);
            const outlineData = {
                outline: response.data.article.outline,
            };
            dispatch(info(outlineData));
            dispatch(next());
            setProgress(100); // Ensure progress bar is full
            clearInterval(interval);
        } catch (error) {
            console.error('Error sending data to backend', error);
            setErrorMessage('出错啦！请稍后再试');
        } finally {
            setIsLoading(false);
            setTimeout(() => setProgress(0), 500); 
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setUploadStatus('Uploading...');
        const formData = new FormData(e.target);
        try {
            const response = await axios.post('http://106.14.184.241/postdata/upload/', formData);
            if (response.status === 201) {
                setUploadStatus('Upload successful!');
                fetchUploadedFiles();
                textInputRef.current.value = "";
                fileInputRef.current.value = "";
            } else {
                setUploadStatus('Upload failed, please try again.');
            }
        } catch (error) {
            setUploadStatus('Error occurred!');
            console.error('Error:', error);
        }
    };

    const handleDeleteAllFiles = async () => {
        try {
            await apiClient.delete('http://106.14.184.241/postdata/upload/');
            setUploadedFiles([]);
            alert('参考资料已清空！');
        } catch (error) {
            console.log('Error:', error);
        }
    };

    const fetchUploadedFiles = async () => {
        try {
            const response = await axios.get('http://106.14.184.241/postdata/upload/');
            setUploadedFiles(response.data.uploaded_files);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="reference">
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
            <div className='uploadedFilesInfo'>
                <div className="uploadedFilesList">
                    <ul className="list-inside">
                        {uploadedFiles.map((file, index) => <li key={index}>{file}</li>)}
                    </ul>
                </div>
                <button onClick={handleDeleteAllFiles}>清空</button>                
            </div>

            <div className={'btnNavigation'}>
                {errorMessage && <div className="error-message">{errorMessage}</div>}
                <button className='btn1' onClick={() => dispatch(back())}>上一步</button>
                <button className='btn3' onClick={GenerateClick} disabled={isLoading}>
                    {/* {isLoading ? '正在生成目录......' : (uploadedFiles.length === 0 ? '跳过上传，直接生成目录' : '生成目录')} */}
                    {/* {isLoading ? <div className="progress-bar"></div> : (uploadedFiles.length === 0 ? '跳过上传，直接生成目录' : '生成目录')} */}
                    <div className="progress-bar" style={{ width: `${progress}%` }}></div>
                    <span>{isLoading ? '正在生成目录......' : (uploadedFiles.length === 0 ? '跳过上传' : '生成目录')}</span>
                </button>
            </div>
        </div>
    );
}

export default Reference;