import React from 'react';
import { fill } from '../features/article';
import axios from 'axios'; 
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';

function Start() {
  const dispatch = useDispatch();
  const navigate = useNavigate();    
  const handleNewTextClick = () => {
    window.location.href = '/preliminary';
  };
  const handleFileUploadClick = async () => { // 添加 async 关键字
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = ".txt, .docx";
    fileInput.onchange = async e => { // 添加 async 关键字
      const file = e.target.files[0];
      if (!file) {
        alert('请你选择文件!');
        return;
      }
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await axios.post('http://106.14.184.241/api/upload/', formData, { // 添加 await 关键字
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        const articleData = {
          content: response.data.article.content
        };
        dispatch(fill(articleData));
        navigate('/article');
      } catch (error) {
        console.error('Error sending data to backend', error);
      }
    };   
    fileInput.click();
  };
  const handleGenerateClick = () => {
    console.log("一键生成 clicked");
    window.location.href = '/oneclickrequirement';
  };
  return (
    <div className="start-container">
      <div className="card card-newtext" onClick={handleNewTextClick}>
        深度定制
      </div>
      <div className="card card-generate" onClick={handleGenerateClick}>
        一键成文
      </div>      
      <div className="card card-fileupload" onClick={handleFileUploadClick}>
        文章润色
      </div>
    </div>
  );
}

export default Start;