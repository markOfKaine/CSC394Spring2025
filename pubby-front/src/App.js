import React, { useEffect, useState } from 'react';
import { getArticles, addArticle, delArticle } from './api';
import './App.css';

function App() {
  const [articles, setArticles] = useState([]);
  const [newArticle, setNewArticle] = useState('');
  const [oldArticle, setOldArticle] = useState('');

  useEffect(() => {
    getArticles().then(res => setArticles(res.data.Message));
  }, []);

  const handleAddArticle = () => {
    if (newArticle.trim() === "") return;
    if (articles.includes(newArticle)) {
      alert("Article already exists");
      return;
    }
    addArticle(newArticle).then(res => {
      setArticles(res.data.Articles);
      setNewArticle('');
    });
  };

  const handleRemoveArticle = () => { 
    if (oldArticle.trim() === "") return;
    if (!articles.includes(oldArticle)) {
      alert("Article does not exist");
      return;
    }
    
    delArticle(oldArticle).then(res => {
      setArticles(prev => prev.filter(article => article !== oldArticle));
      setOldArticle('');
    });
  }

  return (
    <div className="App">
      <header className="App-header">
        <h2 classname="orgName">Baby Pubby</h2>

        <div className="articleInput">
          <input
            type="text"
            value={newArticle}
            onChange={(e) => setNewArticle(e.target.value)}
            placeholder="Enter article name"
          />
          <button onClick={handleAddArticle}>Add Article</button>
        </div>

        <div className="articleInput">
          <input
            type="text"
            value={oldArticle}
            onChange={(e) => setOldArticle(e.target.value)}
            placeholder="Enter article name"
          />
          <button onClick={handleRemoveArticle}>Delete Article</button>
        </div>

        <h2>Article Directory</h2>
        <ul>
          {articles.map((article) => (
            <li key={article}>{article}</li>
          ))}
        </ul>

      </header>
    </div>
  );
}

export default App;
