import time
import streamlit as st


class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if "issue" in metrics:
            return metrics["issue"]

        if exercise == "Squats":
            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)
            
            if depth == "TOO HIGH":
                return "Squat lower, bend your knees more."

            if isinstance(back_angle, (int, float)) and back_angle < 130:
                return "Keep your chest up, don't lean too far forward."

        elif exercise == "Push-ups":
            alignment = metrics.get("body_alignment", "")
            hip_status = metrics.get("hip_status", "")
            
            if alignment == "Poor Form":
                return "Keep your body in a straight line."

            if hip_status == "SAGGING":
                return "Raise your hips, don't let them sag."

            if hip_status == "PIKED UP":
                return "Lower your hips to keep a straight posture."

        elif exercise == "Biceps Curls (Dumbbell)":
            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")
            
            if swing == "SWINGING":
                return "Stop swinging your torso, isolate your biceps."

            if shoulder == "ELBOW DRIFTING":
                return "Keep your elbows glued to your sides."

        elif exercise == "Shoulder Press":
            back_arch = metrics.get("back_arch_status", "")
            extension = metrics.get("extension_status", "")
            
            if back_arch == "Excessive Arch":
                return "Brace your core, avoid arching your back."

            if back_arch == "Slight Arch":
                return "Keep your core tight during the press."

        elif exercise == "Lunges":
            balance = metrics.get("balance_status", "")
            
            if balance == "OFF BALANCE":
                return "Keep your feet hip-width apart for stability."

        return None

    def process_event(self, event, exercise, metrics):
        issue = self._find_form_issue(exercise, metrics)

        now = time.time()
        is_major_issue = event in ["workout_started", "set_completed", "workout_completed"]

        if not is_major_issue:
            if not issue:
                return None
            if now - self.last_spoken_at < 5:
                return None

        text = None
        if self.llm:
            try:
                text = self.llm.give_feedback(event, issue)
            except Exception:
                text = None

        if not text:
            if event == "workout_started":
                text = f"Starting {exercise} workout! Stay focused and maintain good form."
            elif event == "workout_completed":
                text = f"Awesome work! You completed your {exercise} workout."
            elif event == "set_completed":
                text = "Great set! Take a quick breath."
            elif issue:
                text = issue
            else:
                text = "Keep going, great form!"

        voice = self.tts.speak(text)
        self.last_spoken_at = now

        return voice, text


def autoplay_audio(audio_bytes):
    if not audio_bytes:
        return
    st.markdown("<style>[data-testid='stAudio'] {display: none;}</style>", unsafe_allow_html=True)
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
