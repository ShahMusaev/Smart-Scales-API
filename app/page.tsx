'use client'

import { useState, useEffect } from 'react'
import { Avatar } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Plus, User } from 'lucide-react'
import Image from "next/image"
import ProductDetail from "@/app/product-detail";

const weekDays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

const nutritionGoals = {
  calories: { total: 2500 },
  protein: { total: 121 },
  fats: { total: 54 },
  carbs: { total: 161 }
}

interface Product {
  name: string
  calories: number
  protein: number
  fats: number
  carbs: number
  time: string
  image: string
  weight: number
  recommends: any
}

export default function Page() {
  const [selectedDay, setSelectedDay] = useState(new Date())
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProducts(selectedDay)
  }, [selectedDay])

  const fetchProducts = async (date: Date) => {
    setLoading(true)

    try {
      const response = await fetch(`http://localhost:8000/api/products?date=${date.toISOString().split('T')[0]}`)
      if (response.ok) {
        const data = await response.json()
        setProducts(data.products)
      } else {
        setProducts([])
      }
    } catch (error) {
      console.error('Failed to fetch products:', error)
      setProducts([])
    }
    setLoading(false)
  }

  const updateProduct = async (updatedProduct: Product) => {
    try {
      const response = await fetch(`http://localhost:8000/api/products?date=${selectedDay.toISOString().split('T')[0]}/${updatedProduct.name}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedProduct),
      })
      if (response.ok) {
        setProducts(products.map(p => p.name === updatedProduct.name ? updatedProduct : p))
      }
    } catch (error) {
      console.error('Failed to update product:', error)
    }
    setSelectedProduct(null)
  }

  const totalNutrition = products.reduce((acc, product) => ({
    calories: acc.calories + product.calories,
    protein: acc.protein + product.protein,
    fats: acc.fats + product.fats,
    carbs: acc.carbs + product.carbs
  }), { calories: 0, protein: 0, fats: 0, carbs: 0 })

  const caloriesProgress = (totalNutrition.calories / nutritionGoals.calories.total) * 100

  return (
    <div className="max-w-md mx-auto bg-white min-h-screen p-4">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold">Smart Scales</h1>
        <Button variant="ghost" size="icon">
          <User className="h-6 w-6" />
        </Button>
      </div>

      {/* Calendar Week */}
      <div className="flex justify-between mb-8">
        {weekDays.map((day, index) => {
          const date = new Date(selectedDay)
          date.setDate(date.getDate() - date.getDay() + index + (index === 0 ? 1 : 0))
          return (
            <button
              key={day}
              onClick={() => setSelectedDay(date)}
              className={`w-12 h-12 rounded-full flex items-center justify-center ${
                date.toDateString() === selectedDay.toDateString() ? 'bg-black text-white' : 'text-gray-400'
              }`}
            >
              <div className="flex flex-col items-center">
                <span className="text-sm">{day}</span>
                <span className="text-sm">{date.getDate()}</span>
              </div>
            </button>
          )
        })}
      </div>

      {/* Nutrition Card */}
      <Card className="p-6 mb-8">
        <div className="flex items-center gap-8">
          {/* Calories Circle */}
          <div className="relative w-32 h-32">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r="60"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                className="text-gray-100"
              />
              <circle
                cx="64"
                cy="64"
                r="60"
                stroke="currentColor"
                strokeWidth="8"
                fill="none"
                strokeDasharray={377}
                strokeDashoffset={377 - (377 * caloriesProgress) / 100}
                className="text-black"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold">{Math.max(0, nutritionGoals.calories.total - totalNutrition.calories)}</span>
              <span className="text-[0.7rem]">Осталось ккал</span>
            </div>
          </div>

          {/* Nutrition Bars */}
          <div className="flex-1 space-y-4">
            <NutritionBar
              label="Белки"
              current={totalNutrition.protein}
              total={nutritionGoals.protein.total}
              color="bg-[#FF9B9B]"
            />
            <NutritionBar
              label="Жиры"
              current={totalNutrition.fats}
              total={nutritionGoals.fats.total}
              color="bg-[#FFB572]"
            />
            <NutritionBar
              label="Углеводы"
              current={totalNutrition.carbs}
              total={nutritionGoals.carbs.total}
              color="bg-[#4B9AFF]"
            />
          </div>
        </div>
      </Card>

      {/* Recently Added */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Продукты</h2>
        {loading ? (
          <p>Loading...</p>
        ) : products.length === 0 ? (
          <p>Нет продуктов на текущий день.</p>
        ) : (
          products.map((item, index) => (
            <Card key={index} className="p-4">
              <button className="w-full text-left" onClick={() => setSelectedProduct(item)}>
                <div className="flex items-center gap-4">
                  <Image
                    src={item.image}
                    alt={item.name}
                    width={80}
                    height={80}
                    className="rounded-lg"
                  />
                  <div className="flex-1">
                    <div className="flex justify-between items-start">
                      <h3 className="font-semibold">{item.name}</h3>
                      <span className="text-gray-500 text-sm">{item.time}</span>
                    </div>
                    <p className="text-lg font-semibold mb-1">{item.calories} ккал</p>
                    <div className="flex gap-2 text-sm">
                      {/*<span className="px-2 py-1 rounded bg-[#FFE5E5]">Б {item.protein}г</span>*/}
                      <span className="px-2 py-1 rounded bg-[#FF9B9B]">Б {item.protein}г</span>
                      <span className="px-2 py-1 rounded bg-[#FFB572]">Ж {item.fats}г</span>
                      <span className="px-2 py-1 rounded bg-[#4B9AFF]">У {item.carbs}г</span>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">{item.weight}г</p>
                  </div>
                </div>
              </button>
            </Card>
          ))
        )}
      </div>

      {/* Add Button */}
      {/*<div className="fixed bottom-8 left-1/2 -translate-x-1/2">*/}
      {/*  <Button size="lg" className="rounded-full w-12 h-12 bg-black hover:bg-gray-800">*/}
      {/*    <Plus className="h-6 w-6" />*/}
      {/*  </Button>*/}
      {/*</div>*/}

      {/* Product Detail Modal */}
      {selectedProduct && (
        <ProductDetail
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
          onUpdate={updateProduct}
        />
      )}
    </div>
  )
}

function NutritionBar({ label, current, total, color }: {
  label: string
  current: number
  total: number
  color: string
}) {
  const progress = (current / total) * 100

  return (
    <div className="space-y-1.5">
      <div className="flex justify-between text-sm">
        <span>{label}</span>
        <span>{current.toFixed(1)}/{total}г</span>
      </div>
      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full ${color} rounded-full`}
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  )
}

