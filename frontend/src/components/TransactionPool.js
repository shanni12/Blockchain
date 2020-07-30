import React,{useState,useEffect} from 'react';
import {Button } from 'react-bootstrap';
import {Link} from 'react-router-dom';
import Transaction from './Transaction';
import {API_BASE_URL,SECONDS_JS} from '../config';
import history from '../history';
const POOL_INTERVAL=10*SECONDS_JS
function TransactionPool(){
 const [transactions,setTransactions]=useState([]);
 function fetchTransactions(){
    fetch(`${API_BASE_URL}/transactions`).then(response=>response.json()).then(json=>
        
       { console.log('transactions-json',json)
        setTransactions(json)})
 }
 
 function fetchMineBlock(){
     fetch(`${API_BASE_URL}/blockchain/mine`).then(()=>{
         alert('Success');
         history.push('/blockchain');
     })
 }
 
 useEffect(()=>{
     fetchTransactions();
     const intervalId=setInterval(fetchTransactions,POOL_INTERVAL);
     return ()=>clearInterval(intervalId);
     
     
 },[]);
 return (
     <div className="TransactionPool">
         <Link to="/">Home</Link>
         <hr>
         </hr>
         <h3>Transaction Pool</h3>
         <div>
             {
                 transactions.map(transaction=>(<div key={transaction.id}>
                   <hr></hr>
                   <Transaction transaction={transaction}/>
                 </div>))
             }
         </div>
        <hr></hr>
        <Button variant="danger" onClick={fetchMineBlock}> 
            Mine a block of these transactions
        </Button>
     </div>
 )
}
export default TransactionPool;