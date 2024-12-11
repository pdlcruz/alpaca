import React, { useEffect, useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import { StatusBar } from 'expo-status-bar';
import fetch from "node-fetch";
import firebase from 'firebase/app';
import 'firebase/storage';
// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage';

import { Button, Image, StyleSheet, Text, View, TextInput, KeyboardAvoidingView, FlatList, Platform, TouchableOpacity } from 'react-native';

export default function App() {

  const [image, setImage] = useState<string|null>(null);
  const [imageText, setImageText] = useState<string>('');
  const [userQuestion, setUserQuestion] = useState<string>('');
  const [userQuestions, setUserQuestions] = useState<string[]>([]);
  const [ezlegalResponses, setEzlegalResponses] = useState<string[]>([]);

  const [ezlegalPossibleQuestions, setEzlegalPossibleQuestions] = useState<string[]>([]);

  const [responses, setResponses] = useState<{ question: string, answer: string }[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [preQuestionSelected, setPreQuestionSelected] = useState<boolean>(false);

  

  const firebaseConfig = {
    apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
    authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
    projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
    storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.REACT_APP_FIREBASE_APP_ID,
    measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID,
  };



  const app = initializeApp(firebaseConfig);

  const storage = getStorage(app);


  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ['images'],
      allowsEditing: true,
      quality: 1,
    });
  
    if (!result.canceled) {
      console.log("Image picked:", result.assets[0].uri, ); 
      setImage(result.assets[0].uri);
      try {
        // const url = "https://firebasestorage.googleapis.com/v0/b/youbet-48cf2.firebasestorage.app/o/images%2F1733296174325_image.jpg?alt=media&token=b127ec5d-30ba-4f3b-a69b-dea05e06fba4";
        const url = await uploadImage(result.assets[0].uri); // Ensuring this is awaited
        console.log("Uploaded Image URL:", url);
        sendImageUrlToServer(url); 
      } catch (error) {
        console.error("Error uploading image:", error);
      }
    }
  };
  
async function uploadImage(fileUri:string) {
  const filename = `${Date.now()}_image.jpg`; 
  const storageRef = ref(storage, `images/${filename}`);

  try {
     
      const response = await fetch(fileUri);
      const blob = await response.blob(); 
      const snapshot = await uploadBytes(storageRef, blob);
      console.log('Uploaded a blob or file!');

      const downloadURL = await getDownloadURL(snapshot.ref);
      console.log('File available at', downloadURL);
      return downloadURL;
  } catch (error) {
      console.error('Error uploading image:', error);
      throw error;
  }
}

  
  async function sendImageUrlToServer(imageUrl:string) {
    console.log('Sending image URL to server:', imageUrl);
    const response = await fetch('http://10.27.19.122:5003/ocr', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ imageUrl })
    });
  
    const data = await response.json();
    console.log('Data from server:', data);
    setImageText(data.text);
  }


  async function query() {
    setLoading(true);
    const golden_utterance = "MUST FOLLOW THE FOLLOWING RULES: You must answer all of the questions speaking in coloquial spanish. It must be as if you " +
    "are speaking to a highschool  kid who only speaks spanish ";
    const question_sent =  "Given this context text: " + imageText + "\n"+
                         "Answer this question given by the person: " +  userQuestion
    console.log('Querying:', JSON.stringify({
      content: question_sent
  }));
  setEzlegalPossibleQuestions([]);
  const already_generated_questions = userQuestions.concat(ezlegalPossibleQuestions);
  let newQuestions: string[]= [];

  for (let i = 0; i < 1; i++) {
      console.log("generating possible questions:", i);
      const question_to_send = "Given this question being sent : " + question_sent + ". And these questions already generated: " + already_generated_questions.join(', ')
                  + ". Output one possible question that can be asked. Only output the question and nothing else. It is very important that it is in Spanish.";

      console.log("question to send:", question_to_send);
      try {
          const response = await fetch('http://10.27.19.122:3002/query', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                  content: question_to_send
              }),
          });
          const data = await response.json();
          const newQuestion = data.message.content;

          if (!already_generated_questions.includes(newQuestion) && !newQuestions.includes(newQuestion)) {
              newQuestions.push(newQuestion);
          } else {
              console.log('Duplicate question generated, skipping...');
          }
      } catch (error) {
          console.error('Error querying server:', error);
      }
  }

  // Update state once with all new unique questions
  setEzlegalPossibleQuestions(prevQuestions => [...prevQuestions, ...newQuestions]);

    const response = await fetch('http://10.27.19.122:3002/query', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          content: golden_utterance + question_sent
      }),
  }).then((response: { json: () => any; }) => response.json())
    .then((result: { message: { content:string; }; }) => {
      const newResponse = { question: userQuestion, answer: result.message.content as string };
      setResponses(previousResponses => [...previousResponses, newResponse]);
      setUserQuestion('');
      setUserQuestions([...userQuestions, userQuestion]);
      console.log(result.message.content);
      setEzlegalResponses([...ezlegalResponses, result.message.content as string]);
      setLoading(false);
    }).catch((error: any) => {
      console.error('Error querying server:', error);
    });
    const result= await response.json();
    console.log(result);
    return result.message; 
}


interface Item {
  question: string;
  answer: string;
}

const renderItem = ({ item }:{item:Item}) => (
  <View style={styles.message}>
    <Text style={styles.question}>Pregunta: {item.question}</Text>
    <Text style={styles.answer}>Respuesta: {item.answer}</Text>
  </View>
);

  useEffect(() => {
    if (userQuestion && preQuestionSelected) {
      query();
      setPreQuestionSelected(false);
    }
  },[preQuestionSelected, userQuestion]);

  const handleQuestionPress = (question: string) => {
    setUserQuestion(question);
    setPreQuestionSelected(true);
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} style={styles.container}>
      <View style={styles.innerContainer}>
      <Button title="Escogue una Imagen" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={styles.image} />}
      <FlatList
          data={responses}
          renderItem={renderItem}
          keyExtractor={(item, index) => index.toString()}
          contentContainerStyle={styles.list}
        />
        {loading? ( <Text style={{paddingBottom: 30}}>Cargando...</Text>) : (<>
        {ezlegalPossibleQuestions.length > 0 && (
          <View style={styles.message}>
            <Text style={styles.question}> Preguntas Possibles:</Text>
            {ezlegalPossibleQuestions.map((question, index) => (
              <TouchableOpacity key={index} onPress={() => handleQuestionPress(question)} style={styles.questionButton}>
                <Text style={styles.questionText}>{question}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.textInput}
            onChangeText={setUserQuestion}
            value={userQuestion}
            placeholder="Pon tu pregunta aquí"
          />
          <Button title="Pregunte" onPress={query} />
        </View>
        </>)
      }
      </View>
      <StatusBar style="auto" />
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 50,
  },
  innerContainer: {
    flex: 1,
    alignItems: 'center',
  },
  image: {
    width: 200,
    height: 200,
    margin: 10,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    paddingBottom: 30,
  },
  textInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: 'gray',
    marginRight: 10,
    paddingHorizontal: 10,
  },
  message: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  question: {
    fontWeight: 'bold',
  },
  answer: {
    color: 'green',
  },
  list: {
    width: '100%',
  },
  questionButton: {
    backgroundColor: '#ededed',
    padding: 10,
    borderRadius: 5,
    marginTop: 5,
  },
  questionText: {
    color: 'blue',
  }
});
