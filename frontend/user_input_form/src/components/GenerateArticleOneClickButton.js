import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { back } from '../features/pages';
import { fill } from '../features/article';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; 
import apiClient, { setupAxiosInterceptors } from '../interceptors/axioss';

const GenerateArticleOneClickButton = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const description = useSelector((e) => e.description.value);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const article = useSelector((state) => state.article.value);
  
  useEffect(() => {
    setupAxiosInterceptors(navigate, (message) => {
      setErrorMessage(message);
    });
  }, [navigate]);

  const GenerateClick = async () => {
    setIsLoading(true);
    setErrorMessage('');

    try {
      // Use axios for the POST request
      // 127.0.0.1
      // const response = await axios.post('http://106.14.184.241/api/ask/', description, {
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      // });
      const response = await apiClient.post('http://106.14.184.241/api/ask/',  {description, manner: 'oneclick_writting' }, {
        headers: {
          'Content-Type': 'application/json',
        },
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
      // setErrorMessage('出错啦！请稍后再试');        
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={'btnNavigation btnRight'}>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <button className='btn2' onClick={GenerateClick} disabled={isLoading}>
      {isLoading ? '正在生成......' : '生成全文'}
      </button>
    </div>
  );
}

export default GenerateArticleOneClickButton;
