import React, { useState, useEffect } from 'react';
import AugmentTable from './components/AugmentTable';
import SearchBar from './components/SearchBar';

const App = () => {
    const [augments, setAugments] = useState([]);

    useEffect(() => {
        // Fetch all augment data when the component mounts
        fetchAugments();
    }, []);

    const fetchAugments = async () => {
        try {
            // local: const response = await fetch('http://localhost:3000/api/augments/stats');
            const response = await fetch('https://augment-stats-website-80d31fae8bea.herokuapp.com/api/augments/stats');
            const data = await response.json();
            if (Array.isArray(data)) {
                setAugments(data);
            }
        } catch (error) {
            console.error('Error fetching augment data:', error);
            setAugments([]);
        }
    };

    // Fetch augments based on search term
    const handleSearch = async (searchTerm) => {
        if (!searchTerm) {
            fetchAugments(); // If search term is empty, fetch all augments
            return;
        }
        try {
            // local: const response = await fetch(`http://localhost:3000/api/augments/search?term=${encodeURIComponent(searchTerm)}`);
            const response = await fetch(`https://augment-stats-website-80d31fae8bea.herokuapp.com/api/augments/search?term=${encodeURIComponent(searchTerm)}`);
            const data = await response.json();
            if (Array.isArray(data)) {
                setAugments(data);
            }
        } catch (error) {
            console.error('Error fetching search results:', error);
            setAugments([]);
        }
    };

    const refreshData = async () => {
      try {
          // local: const response = await fetch('http://localhost:3000/api/refresh-data', { method: 'POST' });
          const response = await fetch('https://augment-stats-website-80d31fae8bea.herokuapp.com/api/refresh-data', { method: 'POST' });
          
          if (response.ok) {
              console.log('Data refresh initiated');
              fetchAugments(); // Refetch the augment data after refresh
          } else {
              console.error('Failed to initiate data refresh');
          }
      } catch (error) {
          console.error('Error triggering data refresh:', error);
      }
  };

  return (
      <div className="App">
          <h1>Augment Stats</h1>
          <SearchBar onSearch={handleSearch} />
          <button className="refresh-button" onClick={refreshData}>Refresh Data</button>
          <AugmentTable augments={augments} />
      </div>
  );
};

export default App;
