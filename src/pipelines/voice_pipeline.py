from resemblyzer import VoiceEncoder, preprocess_wav
import librosa
import streamlit as st
import numpy as np
import io

@st.cache_resource
def load_voice_encoding():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder=load_voice_encoding()
        
        audio,src=librosa.load(io.BytesIO(audio_bytes),src=16000)
        wav=preprocess_wav(audio)
        embedding=encoder.embed_utterance(wav)
        
        return embedding.tolist() #256 Dime. vector
    
    except Exception as e:
        st.error("Voice recog error")
        return None
    

def identify_speaker(new_embedding,condidate_dict,threshold=0.65):
    if new_embedding is None or not condidate_dict:
        return None,0.0
    
    best_sid=None
    best_score=-1.0
    
    for sid,stored_embedding in condidate_dict.items():
        if stored_embedding:
            similarity=np.dot(new_embedding,stored_embedding)
            if similarity>best_score:
                best_score=similarity
                best_sid=sid
                
    if best_score>=threshold:
        return best_sid,best_score
    
    return None,best_score

    
def process_bulk_audio(audio_bytes,condidates_dict,threshold=0.65):
        
    try:
        encoder=load_voice_encoding()        
        audio,src=librosa.load(io.BytesIO(audio_bytes),src=16000)
        
        segments=librosa.effects.split(audio,top_db=30)
        
        identified_results={}
        
        for start,end in segments:
            if (end-start)<src*0.5:
                continue
            segment_audio=audio[start:end]
            wav=preprocess_wav(segment_audio)
            embedding=encoder.embed_utterarance(wav)
            
            sid,score=identify_speaker(embedding,condidates_dict,threshold)
            
            if sid:
                if sid not in identify_speaker or score>identified_return[sid]:
                    identified_results[sid]=score
                    
        return identified_results
                
            
    except Exception as e:
        st.error('bulk process error')
        return {}
                


