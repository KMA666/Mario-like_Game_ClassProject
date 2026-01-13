#pragma once
#include <SDL2/SDL_mixer.h>
#include <unordered_map>
#include <string>

class AudioManager {
private:
    std::unordered_map<std::string, Mix_Chunk*> soundEffects;
    std::unordered_map<std::string, Mix_Music*> musicTracks;
    
public:
    AudioManager();
    ~AudioManager();
    
    bool initialize();
    void loadSoundEffect(const std::string& name, const std::string& filepath);
    void loadMusic(const std::string& name, const std::string& filepath);
    
    void playSoundEffect(const std::string& name);
    void playMusic(const std::string& name, int loops = -1);
    void stopMusic();
    void pauseMusic();
    void resumeMusic();
    
    void cleanup();
};