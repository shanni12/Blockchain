import React,{useState} from 'react';
import {MILLISECONDS_PY} from '../config';
import Transaction from './Transaction';
import {Button} from 'react-bootstrap';
function ToggleTransactionDisplay({block}){
    const [displayTransaction,setDisplayTransaction]=useState(false);
    const {data}=block;
    function toggleDiaplyTransaction(){
        setDisplayTransaction(!displayTransaction);
    }
    
    
    if(displayTransaction){
       return(<div>
        {data.map(transaction=>(
            <div key={transaction.id}>
                <hr />
                <Transaction transaction={transaction}/>
            </div>
        ))}
        <br></br>
        <Button variant="danger" size="sm" onClick={toggleDiaplyTransaction}>Show Less</Button>
    </div>) 

    }
    return (
        <div>
            <br></br>
            <Button variant="danger" size="sm" onClick={toggleDiaplyTransaction}>Show more</Button>
        </div>
    )
}
function Block({block}){
    const {timestamp,hash,data}=block;
    const hashDisplay=`${hash.substring(0,15)}...`;
    const timestampDisplay=new Date(timestamp/MILLISECONDS_PY).toLocaleString();
      
    return <div className="Block">
               <div>Hash:{hashDisplay}</div>
               <div>Timestamp:{timestampDisplay}</div>
               <ToggleTransactionDisplay block={block}/>
    </div>

}

export default Block;