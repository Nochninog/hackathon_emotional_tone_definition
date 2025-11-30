import styles from './input.module.scss'

function Input({onChange}){
    return(
         <input type="text" placeholder="Введите название файла" onChange={onChange}/>
    )
}

export default Input;