import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View, useWindowDimensions } from 'react-native';


const initial = () => {

    const { width } = useWindowDimensions();
    const isSmallScreen = width < 900; 

    return (
        <View style={styles.container}>
            <TouchableOpacity style={[styles.button, { width: isSmallScreen ? '60%' : '30%' }]}>
                <Text style={styles.buttonText}>Find Churches</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.button, styles.loginButton, { width: isSmallScreen ? '60%' : '30%' }]}>
                <Text style={styles.buttonText}>Login</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.button, styles.signupButton, { width: isSmallScreen ? '60%' : '30%' }]}>
                <Text style={styles.buttonText}>Signup</Text>
            </TouchableOpacity>
        </View>
    );
};


const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 20,
        marginTop: 50, 
        paddingVertical: 0,
    },
    button: {
        backgroundColor: '#6200ee', 
        paddingVertical: 15,
        paddingHorizontal: 30,
        borderRadius: 25, 
        marginVertical: 10,
        alignItems: 'center',
    },
    loginButton: {
        backgroundColor: '#03DAC6', 
    },
    signupButton: {
        backgroundColor: '#018786', 
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: 'bold',
    },
});


export default initial