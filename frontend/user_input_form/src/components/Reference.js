import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Reference() {
    const [uploadStatus, setUploadStatus] = useState('');
    const [uploadedFiles, setUploadedFiles] = useState([]);

    useEffect(() => {
        fetchUploadedFiles();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setUploadStatus('Uploading...');
        const formData = new FormData(e.target);

        try {
            await axios.post('http://localhost:8000/postdata/upload/', formData);
            setUploadStatus('Upload successful!');
            fetchUploadedFiles();
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
            <h2>Reference</h2>
            {/* <h3>You can upload your references here</h3> */}
            <form className="uploadForm" encType="multipart/form-data" onSubmit={handleSubmit}>
                <div className="fields">
                    <label id="reference_text" htmlFor="text">Text:</label>
                    <textarea id="text" name="text" placeholder="Text"></textarea>
                </div>
                <div className="fields">
                    <label htmlFor="file"> File (pdf,txt,doc):</label>
                    <input 
                        type="file" 
                        id="single_file" 
                        name="single_file" 
                        accept=".pdf, .txt, .docx" 
                    />
                </div>
                <div className="fields">
                    <label htmlFor="website">Website URL:</label>
                    <input
                        type="url" 
                        id="website" 
                        name="website" 
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