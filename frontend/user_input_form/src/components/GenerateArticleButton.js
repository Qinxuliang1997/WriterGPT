import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { back } from '../features/pages';
import { fill } from '../features/article';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; 

const GenerateArticleButton = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const description = useSelector((e) => e.description.value);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const article = useSelector((state) => state.article.value);

  const GenerateClick = async () => {
    setIsLoading(true);
    setErrorMessage('');

    try {
      // Use axios for the POST request
      const response = await axios.post('http://127.0.0.1:8000/api/ask/', description, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log('成功发送：', response.data);
      const articleData = {
        title:response.data.article.title,
        content: response.data.article.content
      };
      dispatch(fill(articleData));
      navigate('/article');
    } catch (error) {
      console.error('Error sending data to backend', error);
      setErrorMessage('出错啦！请稍后再试');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={'btnNavigation'}>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <button className='btn1' onClick={() => dispatch(back())}>上一步</button>
      <button className='btn2' onClick={GenerateClick} disabled={isLoading}>
        {isLoading ? '正在生成......' : '生成全文'}
      </button>
    </div>
  );
}

export default GenerateArticleButton;
