import { useState } from "react";

export default function SearchCoins({ getSearchResults }) {
   const [query, setQuery] = useState('');

   const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // const response = await fetch(`/api/search?query=${query}`);
      const response = await fetch(`/search?query=${query}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const coin = await response.json();
      getSearchResults(coin);
    } catch (error) {
      console.error('Error fetching search results:', error);
      // Handle error (e.g., display error message to user)
    }
   };

  return (
    <div className="text-center my-20">
        <form onSubmit={handleSubmit}>
            <input className="text-black border-2 border-black rounded-full px-3 py-2" type="text" placeholder="Search coin..." value={query} onChange={(e) => setQuery(e.target.value)} />
            <button className="bg-black text-white rounded-full px-3 py-2 hover:bg-black/60" type="submit">Search</button>
        </form>
    </div>
  );
}
