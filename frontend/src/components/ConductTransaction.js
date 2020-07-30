import React,{useState,useEffect} from 'react';
import {FormGroup,FromControl,Button, FormControl} from 'react-bootstrap';
import {API_BASE_URL} from '../config';
import {Link} from 'react-router-dom';
import history from '../history';
function ConductTransaction(){
  const [amount,setAmount]=useState(0);
  const [recipient,setRecipient]=useState('');
  const [knownAddresses,setKnownAddresses]=useState([]);

  useEffect(() =>{
      fetch(`${API_BASE_URL}/known-addresses`).then(response=>response.json()).then(json=>setKnownAddresses(json))
  },[])
  
  function updateRecipient(event){
      setRecipient(event.target.value);
  }
  
  
  function updateAmount(event){
    setAmount(Number(event.target.value));
   }
  
  
  
   function submitTransaction(){
      fetch(`${API_BASE_URL}/wallet/transact`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({recipient,amount})
    }).then(response=>response.json()).then(json=>{console.log('submit Transactionjson',json);
       alert('Success');
       history.push('/transaction-pool');
    })
  }
  
  
  return (
      <div className="ConductTransaction">
          <Link to='/'>Home</Link>
          <hr></hr>
          <h3>Conduct a Transaction</h3>
          <br></br>
          <FormGroup>
              <FormControl 
              input="text"
              placeholder="recipient"
              value={recipient}
              onChange={updateRecipient}
              />
          </FormGroup>
          <FormGroup>
              <FormControl 
              input="nummber"
              placeholder="amount"
              value={amount}
              onChange={updateAmount}
              />
          </FormGroup>
          <div>
              <Button variant="danger" onClick={submitTransaction}>
                  Submit
              </Button>
          </div>
          <br></br>
          <h4>Known Addresses</h4>
          <div>
  {knownAddresses.map((knownAddress,i)=>(<span key={knownAddress}><u>{knownAddress}</u>{ i !==knownAddresses.length-1?', ':'' }</span>))}
          </div>
      </div>
  )
}
export default ConductTransaction;