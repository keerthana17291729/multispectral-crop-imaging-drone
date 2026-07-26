import axios from "axios"

const API = axios.create({
baseURL:"http://127.0.0.1:8000"
})

export const uploadImage = async(file)=>{

const form = new FormData()

form.append("file",file)
form.append("objectives","classification")

const res = await API.post("/analyze",form)

return res.data

}

export const analyzeObjectives = async(file,obj)=>{

const form = new FormData()

form.append("file",file)
form.append("objectives",obj)

const res = await API.post("/analyze",form)

return res.data

}